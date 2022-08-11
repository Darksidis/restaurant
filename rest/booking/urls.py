
from django.contrib import admin
from django.urls import path
from . import views


app_name = 'booking'
urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    path('', views.post_list, name='list_tables'),
    path('<int:number>/', views.table_detail, name='table_detail'),
    path('<int:number>/reservation/', views.table_reservation, name='table_reservation'),
    path('<int:number>/cancel_booking', views.cancel_booking, name='cancel_booking')
]
