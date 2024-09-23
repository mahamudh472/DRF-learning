from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('person2', views.AnotherList)

urlpatterns = [
    path('person/', views.PersonList.as_view(), name='person'),
    path('', include(router.urls))
]