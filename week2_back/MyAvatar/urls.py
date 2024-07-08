from django.urls import path
from . import views

urlpatterns = [
    path('save_kakao_user/', views.save_kakao_user, name='save_kakao_user'),
    path('search_user/', views.search_user, name='search_user'),
    path('get_items/', views.get_items, name='get_items'),
    path('add_friend/', views.add_friend, name='add_friend'),
    path('get_friends/<str:user_id>', views.get_friends, name='get_friends'),
    path('get_friend_requests/<str:user_id>', views.get_friend_requests, name='get_friend_requests'),
    path('accept_friend_request/', views.accept_friend_request, name='accept_friend_request'),
]
