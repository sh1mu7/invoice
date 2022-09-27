from django.urls import path
from .views import home
app_name = 'invoice'

urlpatterns = [
    path('',home,name='home')
]
