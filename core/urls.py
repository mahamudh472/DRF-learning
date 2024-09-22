from django.urls import path
from . import views

urlpatterns = [
    path('person/', views.PersonList.as_view(), name='person')
]