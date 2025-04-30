from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from events.views import register, user_login  # Импортируем user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Встроенные маршруты
    path('accounts/register/', register, name='register'),  # Кастомный маршрут для регистрации
    path('accounts/login/', user_login, name='login'),  # Кастомный маршрут для входа
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)