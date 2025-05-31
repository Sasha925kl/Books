from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, Http404
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm

from .models import Room, Booking, Property, Comment, Rating  # добавь Rating, если есть модель
from .forms import (
    BookingForm,
    PropertySearchForm,
    SearchForm,
    CommentForm,
    ProfileUpdateForm,
    CustomPasswordChangeForm,
)

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def home(request):
    rooms = Room.objects.all()
    form = SearchForm()
    return render(request, 'home.html', {'rooms': rooms, 'form': form})

def available_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'available_rooms.html', {'rooms': rooms})

def search_results(request):
    query = request.GET.get('location', '').strip()
    rooms = Room.objects.filter(location__icontains=query) if query else Room.objects.all()
    return render(request, 'search/search_results.html', {'rooms': rooms, 'query': query})

@login_required
def create_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.user = request.user
            booking.save()
            return redirect('success')
    else:
        form = BookingForm()

    return render(request, 'booking/create_booking.html', {'form': form, 'room': room})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = BookingForm()
    return render(request, 'booking_form.html', {'form': form})

def profile_view(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('start_time')
    context = {
        'bookings': bookings
    }
    return render(request, 'profile.html', context)

def success_view(request):
    return render(request, 'success.html')

def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    comments = property.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.property = property
            comment.user = request.user
            comment.save()
            return redirect('property_detail', property_id=property.id)
    else:
        form = CommentForm()

    return render(request, 'property_detail.html', {
        'property': property,
        'comments': comments,
        'form': form,
    })

@login_required
def add_rating(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        Rating.objects.create(user=request.user, room=room, rating=rating)
        return redirect('search_results')
    return render(request, 'booking/add_rating.html', {'room': room})

@login_required
def add_comment(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        text = request.POST.get('comment', '').strip()
        if text:
            Comment.objects.create(user=request.user, room=room, text=text)
        return redirect('search_results')
    return render(request, 'booking/add_comment.html', {'room': room})

@login_required
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        raise Http404("Коментар не знайдено")

    if comment.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden("Ви не можете видаляти цей коментар")

    if request.method == 'POST':
        property_id = comment.property.id
        comment.delete()
        return redirect('property_detail', property_id=property_id)

    return render(request, 'confirm_delete_comment.html', {'comment': comment})

@method_decorator(csrf_exempt, name='dispatch')
class LogoutGetAllowedView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профіль оновлено.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'profile/profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль змінено успішно.')
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'users/change_password.html', {'form': form})
