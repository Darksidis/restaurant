from celery import shared_task
from django.core.mail import send_mail
from django.utils.html import strip_tags


@shared_task
def send_info(html_message, cd_email):
    """Задача отправки email-уведомлений при бронирований столика"""

    subject = 'Вы забронировали столик'
    message = strip_tags(html_message)

    return send_mail(
        subject,
        message,
        'imperius14888@yandex.ru',
        [cd_email],
        html_message=html_message,
    )
