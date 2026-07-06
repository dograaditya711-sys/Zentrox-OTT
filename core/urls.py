from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Yeh home page ka route hai
path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
path('search/', views.search, name='search'), # YEH NAYI LINE HAI
path('series/', views.tv_home, name='tv_home'), # Web series ka homepage
    path('series/<int:pk>/', views.tv_detail, name='tv_detail'),
path('anime/', views.anime_home, name='anime_home'),
path('actor/<int:actor_id>/', views.actor_movies, name='actor_movies'),
]