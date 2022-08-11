# restaurant

About
-------

An API service that will accept orders for table reservations in a restaurant.

What did I use
-------

Django, Celery/RabbitMQ, PostgreSQL

How it works
--------

- #### Administrative functions:
Set a reservation, cancel a reservation, close a table for a reservation, set the cost of a reservation, add/change a table.

- #### Public Functions:
Selection of a table, reservation order (indicating the client's e-mail and phone number), cancellation of the reservation order (via the button in the client's e-mail message about accepting the reservation order). Selection options: table type, number of seats, cost range.

## Project setup
```
pip install pipenv
python -m pipenv install
```

## Compiles 
```
python -m pipenv shell
python manage.py runserver
```
