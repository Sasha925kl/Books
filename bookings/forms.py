from django import forms
from .models import Booking, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['start_time', 'end_time', 'comment']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Комментарий (необязательно)'}),
        }

class PropertySearchForm(forms.Form):
    location = forms.CharField(required=False, label="Местоположение")
    check_in = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Дата заезда")
    check_out = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label="Дата выезда")
    guests = forms.IntegerField(required=False, min_value=1, label="Гостей")
    min_price = forms.DecimalField(required=False, min_value=0, label="Цена от")
    max_price = forms.DecimalField(required=False, min_value=0, label="Цена до")

class SearchForm(forms.Form):
    location = forms.CharField(
        label='Куда поедем?',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Например, Київ или Львів'
        })
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Оставьте ваш комментарий...'})
        }

class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(label="Нікнейм")

    class Meta:
        model = User
        fields = ['username', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Старий пароль'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Новий пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Підтвердіть новий пароль'}))