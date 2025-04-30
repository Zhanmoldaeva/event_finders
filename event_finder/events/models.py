from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    is_organizer = models.BooleanField(default=False, help_text="Указывает, является ли пользователь организатором.")

    def __str__(self):
        return self.username

class Venue(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.city})"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=False)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    downloadable_file = models.FileField(upload_to='event_files/', null=True, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', null=True)  # Новое поле

    def __str__(self):
        return f"{self.name} - {self.date}"

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

class EventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], help_text="Оценка от 1 до 5")
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.event.name} ({self.rating})"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

class Quiz(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название викторины")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Викторина"
        verbose_name_plural = "Викторины"

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('single', 'Одиночный выбор'),
        ('multiple', 'Множественный выбор'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions', verbose_name="Викторина")
    text = models.TextField(verbose_name="Текст вопроса")
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPE_CHOICES, default='single', verbose_name="Тип вопроса")
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True, verbose_name="Изображение")
    # Варианты ответа
    option_1 = models.CharField(max_length=200, verbose_name="Вариант 1")
    option_2 = models.CharField(max_length=200, verbose_name="Вариант 2")
    option_3 = models.CharField(max_length=200, verbose_name="Вариант 3", blank=True)
    option_4 = models.CharField(max_length=200, verbose_name="Вариант 4", blank=True)
    # Правильные ответы (индексы, начиная с 1: 1 для option_1, 2 для option_2 и т.д.)
    correct_answers = models.CharField(max_length=50, verbose_name="Правильные ответы (индексы через запятую, например: 1 или 1,2)")

    def get_options(self):
        options = [self.option_1, self.option_2]
        if self.option_3:
            options.append(self.option_3)
        if self.option_4:
            options.append(self.option_4)
        return options

    def get_correct_answers(self):
        return [int(idx) for idx in self.correct_answers.split(',')]

    def __str__(self):
        return f"Вопрос: {self.text[:50]}..."

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    selected_answers = models.CharField(max_length=50, verbose_name="Выбранные ответы (индексы через запятую)")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата ответа")

    def __str__(self):
        return f"Ответ {self.user.username} на вопрос {self.question.text[:50]}..."

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "Ответы пользователей"