from django.urls import path
from . import views

urlpatterns = [
    path('speech/', views.speech, name='speech'),
]