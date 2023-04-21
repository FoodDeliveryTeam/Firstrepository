from django.urls import path,include
from .views import Dashboard

urlpatterns=[
    path('dashboard/',Dashboard.as_view(),name='dashboard'),

]