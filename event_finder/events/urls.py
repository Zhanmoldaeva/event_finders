from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('search/', views.search, name='search'),
    path('event/<int:event_id>/buy/', views.buy_ticket, name='buy_ticket'),
    path('event/<int:event_id>/register/', views.register_event, name='register_event'),
    path('profile/', views.profile, name='profile'),
    path('feedback/<int:ticket_id>/', views.feedback, name='feedback'),
    path('chat/', views.chat_bot, name='chat_bot'),
    path('create-event/', views.create_event, name='create_event'),
    path('accounts/login/', views.user_login, name='login'),  # Кастомный маршрут для входа
    path('accounts/register/', views.register, name='register'),  # Кастомный маршрут для регистрации
    path('check-auth/', views.check_auth, name='check_auth'),  # Маршрут для проверки авторизации
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
]