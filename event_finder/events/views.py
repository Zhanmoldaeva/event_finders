
from django.contrib.auth import authenticate, login
from .models import Event, Ticket, Registration, User, EventFeedback
from django.db import models
from .forms import LoginForm, RegisterForm, TicketPurchaseForm, EventFeedbackForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .forms import EventForm
from django.contrib import messages
# Главная страница
def home(request):
    events = Event.objects.filter(date__gte=timezone.now()).order_by('date')
    return render(request, 'events/home.html', {'events': events})

# Детали события
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def create_event(request):
    if not request.user.is_organizer:
        messages.error(request, "Только организаторы могут создавать мероприятия.")
        return HttpResponseForbidden("У вас нет прав для создания мероприятия.")

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Устанавливаем организатора
            event.save()
            messages.success(request, "Мероприятие успешно создано!")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})
# Поиск событий
def search(request):
    query = request.GET.get('q', '')
    events = Event.objects.filter(
        models.Q(name__icontains=query) |
        models.Q(venue__city__icontains=query) |
        models.Q(category__name__icontains=query)
    ).filter(date__gte=timezone.now())
    return render(request, 'events/search.html', {'events': events, 'query': query})

# Покупка билетов
@login_required
def buy_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.is_free:
        messages.error(request, "Это событие бесплатное. Используйте регистрацию.")
        return redirect('events:event_detail', event_id=event.id)

    if request.method == 'POST':
        form = TicketPurchaseForm(request.POST, event=event)
        if form.is_valid():
            ticket = form.save(user=request.user)
            messages.success(request, "Билеты успешно приобретены!")
            return redirect('events:feedback', ticket_id=ticket.id)  # Перенаправление на опрос
    else:
        form = TicketPurchaseForm(event=event)
    return render(request, 'events/buy_ticket.html', {'event': event, 'form': form})

# Регистрация на бесплатное событие
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if not event.is_free:
        messages.error(request, "Это событие платное. Купите билет.")
        return redirect('events:event_detail', event_id=event.id)

    if Registration.objects.filter(event=event, user=request.user).exists():
        messages.info(request, "Вы уже зарегистрированы на это событие.")
    else:
        Registration.objects.create(event=event, user=request.user)
        messages.success(request, "Вы успешно зарегистрированы!")
    return redirect('events:profile')

# Профиль пользователя
@login_required
def profile(request):
    tickets = Ticket.objects.filter(user=request.user)
    registrations = Registration.objects.filter(user=request.user)
    return render(request, 'events/profile.html', {
        'tickets': tickets,
        'registrations': registrations
    })
import time
# Регистрация пользователя
# Регистрация
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .forms import RegisterForm  # Импортируем форму
from .models import User
import time

# ... остальные импорты ...

def register(request):
    if request.method == 'POST':
        # Фиксируем время окончания процесса
        end_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        start_time = int(request.POST.get('start_time', end_time))  # Время начала из формы
        time_spent = (end_time - start_time) / 1000  # Время в секундах

        form = RegisterForm(request.POST, request.FILES)  # Используем форму
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя через форму
            login(request, user)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': reverse('events:home'),
                    'time_spent': round(time_spent, 2)
                })
            messages.success(request, f'Регистрация прошла успешно! Время: {round(time_spent, 2)} секунд.')
            return redirect('events:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Ошибка регистрации. Проверьте введённые данные.',
                    'errors': form.errors.as_json(),
                }, status=400)
            messages.error(request, 'Ошибка при регистрации. Проверьте введённые данные.')
            return render(request, 'events/register.html', {'form': form})

    form = RegisterForm()
    return render(request, 'events/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        # Фиксируем время окончания процесса
        end_time = int(time.time() * 1000)  # Текущее время в миллисекундах
        start_time = int(request.POST.get('start_time', end_time))  # Время начала из формы
        time_spent = (end_time - start_time) / 1000  # Время в секундах

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': '/',
                    'time_spent': round(time_spent, 2)
                })
            messages.success(request, f'Вы успешно вошли! Время: {round(time_spent, 2)} секунд.')
            return redirect('events:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Неверное имя пользователя или пароль.'})
            messages.error(request, 'Неверное имя пользователя или пароль.')
            return render(request, 'events/login.html')

    return render(request, 'events/login.html')

def check_auth(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_authenticated': request.user.is_authenticated
        })
    return JsonResponse({'error': 'Недопустимый запрос'}, status=400)

# Опрос после покупки билета
@login_required
def feedback(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    event = ticket.event

    if EventFeedback.objects.filter(event=event, user=request.user).exists():
        messages.info(request, "Вы уже оставили отзыв на это событие.")
        return redirect('events:profile')

    if request.method == 'POST':
        form = EventFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.event = event
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Спасибо за ваш отзыв!")
            return redirect('events:profile')
    else:
        form = EventFeedbackForm()
    return render(request, 'events/feedback.html', {'form': form, 'event': event})


import aiohttp
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import ChatMessage, Event
from django.db.models import Q
from asgiref.sync import sync_to_async
from django.utils import timezone

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Вы успешно вышли из системы.')
        return redirect('events:home')
    return redirect('events:home')

@login_required
async def chat_bot(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        if user_message:
            # Проверка на запрос о событиях
            if "события" in user_message.lower() or "мероприятия" in user_message.lower():
                query = user_message.split()[-1]
                events = await sync_to_async(
                    lambda: list(Event.objects.filter(
                        Q(name__icontains=query) | Q(venue__city__icontains=query)
                    ))
                )()
                if events:
                    bot_response = "Вот что я нашел:\n" + "\n".join(
                        [f"{e.name} - {e.date} ({e.venue.city})" for e in events[:3]]
                    )
                else:
                    bot_response = "К сожалению, ничего не найдено."
                await sync_to_async(ChatMessage.objects.create)(
                    user=request.user,
                    message=user_message,
                    response=bot_response
                )
            else:
                messages_history = await sync_to_async(
                    lambda: list(ChatMessage.objects.filter(user=request.user).select_related('user').order_by('timestamp')[:5])
                )()
                conversation = [
                    {"role": "user", "content": msg.message} for msg in messages_history
                ] + [{"role": "user", "content": user_message}]

                url = "https://api.deepseek.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": "deepseek-chat",
                    "messages": conversation,
                    "max_tokens": 500,
                    "temperature": 0.7,
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            bot_response = data['choices'][0]['message']['content']
                        else:
                            bot_response = f"Ошибка: {response.status} - {await response.text()}"
                        await sync_to_async(ChatMessage.objects.create)(
                            user=request.user,
                            message=user_message,
                            response=bot_response
                        )

            messages = await sync_to_async(
                lambda: list(ChatMessage.objects.filter(user=request.user).select_related('user').order_by('timestamp'))
            )()
            messages_data = [
                {
                    'username': msg.user.username,
                    'message': msg.message,
                    'response': msg.response,
                    'timestamp': msg.timestamp.strftime('%d %B %Y, %H:%M')  # Форматируем время
                } for msg in messages
            ]
            return render(request, 'events/chatbot.html', {'messages': messages_data})

    messages = await sync_to_async(
        lambda: list(ChatMessage.objects.filter(user=request.user).select_related('user').order_by('timestamp'))
    )()
    messages_data = [
        {
            'username': msg.user.username,
            'message': msg.message,
            'response': msg.response,
            'timestamp': msg.timestamp.strftime('%d %B %Y, %H:%M')  # Форматируем время
        } for msg in messages
    ]
    return render(request, 'events/chatbot.html', {'messages': messages_data})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event, Venue, Category, Quiz, Question, UserAnswer
from .forms import EventForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import time

# ... остальные представления ...

# Список викторин
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'events/quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        total_questions = questions.count()
        user_answers = []

        for question in questions:
            selected_answer_ids = request.POST.getlist(f'question_{question.id}')
            selected_answer_ids = [int(idx) for idx in selected_answer_ids]

            # Сохраняем ответ пользователя
            user_answer = UserAnswer.objects.create(
                user=request.user,
                question=question,
                selected_answers=','.join(map(str, selected_answer_ids))
            )

            # Проверяем правильность ответа
            correct_answer_ids = question.get_correct_answers()
            is_correct = False
            if question.question_type == 'single':
                if len(selected_answer_ids) == 1 and selected_answer_ids[0] in correct_answer_ids:
                    score += 1
                    is_correct = True
            else:  # multiple
                if set(selected_answer_ids) == set(correct_answer_ids):
                    score += 1
                    is_correct = True

            # Собираем данные для анализа
            user_answers.append({
                'question': question,
                'selected_answers': selected_answer_ids,
                'correct_answers': correct_answer_ids,
                'is_correct': is_correct,
            })

        # Подготавливаем результат
        result = {
            'score': score,
            'total': total_questions,
            'percentage': (score / total_questions) * 100 if total_questions > 0 else 0,
            'user_answers': user_answers,
        }
        return render(request, 'events/quiz_result.html', {'quiz': quiz, 'result': result})

    return render(request, 'events/quiz_detail.html', {'quiz': quiz, 'questions': questions})