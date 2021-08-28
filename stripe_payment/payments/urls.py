from django.urls import path

from .views import create_charge, capture_charge, create_refund, get_charges


app_name = 'payments'

urlpatterns = [
    path('create_charge', create_charge, name='create-charge'),
    path('capture_charge/<str:chargeId>', capture_charge, name='capture-charge'),
    path('create_refund/<str:chargeId>', create_refund, name='create-refund'),
    path('get_charges', get_charges, name='get-charges'),
]
