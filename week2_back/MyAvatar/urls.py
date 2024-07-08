from django.urls import path
from .views import save_kakao_user

urlpatterns = [
    path('save_kakao_user/', save_kakao_user, name='save_kakao_user'),
]
