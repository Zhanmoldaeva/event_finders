from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Venue, Category, Event, Ticket, Registration, EventFeedback, ChatMessage, Quiz, Question, \
    UserAnswer


# Кастомный UserAdmin для отображения дополнительных полей
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_organizer', 'city', 'is_staff')
    list_filter = ('is_organizer', 'is_staff')
    search_fields = ('username', 'email')

    # Поля, отображаемые в форме редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'profile_picture', 'city')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_organizer', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля, отображаемые при создании нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_organizer', 'city', 'profile_picture'),
        }),
    )

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    search_fields = ('name', 'city')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue', 'organizer')
    list_filter = ('date', 'venue', 'organizer')
    search_fields = ('name', 'description')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'purchase_date')
    list_filter = ('purchase_date',)
    search_fields = ('user__username', 'event__name')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'registration_date')
    list_filter = ('registration_date',)
    search_fields = ('user__username', 'event__name')

@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'event__name')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('user__username', 'message')


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'question_type')
    list_filter = ('quiz', 'question_type')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'submitted_at')
    list_filter = ('user', 'question')