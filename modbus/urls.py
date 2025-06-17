from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.modbus),
    path('modbus_data', views.modbus_data, name='modbus_data'),
    ]
