from django.urls import path
from . import views

urlpatterns = [
    #Orders urls
    path("place_order/", views.place_order, name="place_order"), 

    #payments urls
    path("payments/", views.payments, name="payments"),

    #order complete urls
    path("order_complete/", views.order_complete, name="order_complete"),

]
