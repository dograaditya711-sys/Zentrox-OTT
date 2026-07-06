from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Naya account banane ka raasta
    path('register/', views.register, name='register'),
    
    # Django ka apna bana-banaya Login system
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # Logout hone ke baad wapas home page par bhej do
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile, name='profile'),

    # WATCHLIST API ROUTES
    path('watchlist/add/', views.add_to_watchlist, name='add_watchlist'),
    path('watchlist/remove/', views.remove_from_watchlist, name='remove_watchlist'),
]