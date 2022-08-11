from django.shortcuts import render, get_object_or_404
from .models import Table, Client
from .forms import EmailPostForm
from django.http import HttpRequest
from .tasks import send_info
from .regular_mail_delivery import regular_send
from django.template.loader import render_to_string
from django.conf import settings


def post_list(request: HttpRequest):
    """
    Возвращаем все столики (вместе с ссылками на бронирование)
    с помощью менеджера published, а так же параметры подбора
    (подбор столика, количество мест, диапазон стоимости)
     """

    tables = Table.published.all()

    # Получает список типов
    types = list(set([str(table.type) for table in tables]))
    # Добавляем вкладку 'все' для отображения всех столиков, ставим его на первое место
    types.insert(0, 'все')

    # Количество стульев
    seats = [int(table.seats) for table in tables]
    seats.sort()

   # Формирование диапазона цены
    prices = [str(table.booking_price) for table in tables]
    prices.sort()

    if tables:
        seats = [str(seats[0]), str(seats[-1])]
        prices = prices[-1]
    # значения по умолчанию для параметра "количество мест" и "стоимость"
    value_range_price = '0'
    seats_table = ''
    if request.method == 'POST':
        type_table = request.POST.get('type_table', '')
        seats_table = request.POST.get('seats_table', '')
        prices_table = request.POST.get('prices_table', '')

        #если в post форме введены данные, мы фильтруем список столиков
        if seats_table:
            tables = tables.filter(seats=seats_table)
        if prices_table != '0':
            tables = tables.filter(booking_price=prices_table)
            value_range_price = prices_table
        if type_table != 'все':
            tables = tables.filter(type__type=type_table)

        # алгоритм, с помощью которого список видов столиков будет всегда выстроен по порядку
        replace_el = types.index(type_table)
        first_el = 0
        types[first_el], types[replace_el] = types[replace_el], types[first_el]

    return render(request, 'booking/post/list.html', {
        'seats_table': seats_table,
        'value_range_price': value_range_price,
        'prices': prices,
        'seats': seats,
        'types': types,
        'tables': tables,
    })


def table_reservation(request, number):
    """
    В этой функций происходит бронирование столика,
    занос данных клиента в базу, и отправка на почту html-формы.
    """
    # Retrieve post by id
    table = get_object_or_404(Table, number=number, status_published='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Если форма валидна, мы идём дальше
            cd = form.cleaned_data

            html_message = render_to_string(
                'booking/email/mail_template.html',
                {
                    'table': table,
                },
                request=request,
            )
            # Если в настройках указано, что должжен быть включен celery, вызывается асинхронная задача
            if settings.STATUS_CELERY == True:
                # вызываем асинхронную задачу
                send_info.delay(html_message, cd['email'])
            else:
                regular_send(html_message, cd['email'])

            sent = True


            # в этом разделе обновляем базу
            client = Client.objects.filter(
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
            )
            # В случае, если клиент ранее не бронировал столик, то создается новая запись
            if not client.exists():
                Client(
                    name=cd['name'],
                    email=cd['email'],
                    phone=cd['phone'],
                ).save()
            # Cтолик теперь с точки зрения БД будет "занят"

            table.status_booking = client.get()
            table.status_published = 'draft'
            table.save()
    else:
        form = EmailPostForm()
    return render(request, 'booking/post/share.html', {'table': table, 'form': form, 'sent': sent})


def table_detail(request, number):
    """
    В этом разделе должна содержаться
    более подробная информация о столике
    """
    return render(request, 'booking/post/detail.html', {'number': number})


def cancel_booking(request, number):
    """
    Отменяет бронирование столика. С точки зрения БД меняет
    статус бронирования на Null, и публикует столик заново
    """

    table = get_object_or_404(Table, number=number, status_published='draft')

    # Пользователь отвязывается от столика
    table.status_booking = None
    table.status_published = 'published'
    table.save()
    return render(request, 'booking/post/cancel_booking.html', {'table': table})
