from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.shortcuts import render


class LogoutGetAllowedView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

urlpatterns = [
    path('', views.home, name='home'),
    path('available_rooms/', views.available_rooms, name='available_rooms'),

    #
    path('rooms/<int:room_id>/booking/', views.create_booking, name='create_booking'),

    path('register/', views.register, name='register'),

    path('logout/', LogoutGetAllowedView.as_view(next_page='home'), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    path('search_results/', views.search_results, name='search_results'),

    path('booking/', views.booking_view, name='booking'),  

    path('success/', views.success_view, name='success'),

    path('property/<int:property_id>/', views.property_detail, name='property_detail'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/change-password/', views.change_password_view, name='change_password'),

    path('bookings/', views.booking_view, name='bookings'),

    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),

    path('rooms/<int:room_id>/add-rating/', views.add_rating, name='add_rating'),
    path('rooms/<int:room_id>/add-comment/', views.add_comment, name='add_comment'),
]


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
