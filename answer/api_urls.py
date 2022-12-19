from django.urls import path
from .views import answer_list

urlpatterns = [
    path('list/', answer_list)
]