from django.urls import path
from . import views

urlpatterns = [
    path('save_kakao_user/', views.save_kakao_user, name='save_kakao_user'),
    path('search_user/', views.search_user, name='search_user'),
]
