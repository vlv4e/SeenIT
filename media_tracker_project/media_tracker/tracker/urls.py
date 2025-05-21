# tracker/urls.py
from django.urls import path
from .views import (
    register, log_show, log_movie, home,
    movie_list, movie_create, movie_update, movie_delete,
    show_list, show_create, show_update, show_delete, show_favorite, show_favorite_list,
    movie_favorite, movie_favorite_list,
    to_watch_show_list, to_watch_show_update, to_watch_show_delete,  # Import to_watch show views
    to_watch_movie_list, to_watch_movie_update, to_watch_movie_delete  # Import to_watch movie views
)
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('log_show/', log_show, name='log_show'),
    path('log_movie/', log_movie, name='log_movie'),
    path('', home, name='home'),

    # Movie URLs
    path('movies/', movie_list, name='movie_list'),
    path('movies/create/', movie_create, name='movie_create'),
    path('movies/update/<int:pk>/', movie_update, name='movie_update'),
    path('movies/delete/<int:pk>/', movie_delete, name='movie_delete'),
    path('movies/<int:pk>/favorite/', movie_favorite, name='movie_favorite'),
    path('movies/favorites/', movie_favorite_list, name='movie_favorite_list'),

    # Show URLs
    path('shows/', show_list, name='show_list'),
    path('shows/create/', show_create, name='show_create'),
    path('shows/update/<int:pk>/', show_update, name='show_update'),
    path('shows/delete/<int:pk>/', show_delete, name='show_delete'),
    path('shows/<int:pk>/favorite/', show_favorite, name='show_favorite'),
    path('shows/favorites/', show_favorite_list, name='show_favorite_list'),

    # To Watch Show URLs
    path('to_watch/shows/', to_watch_show_list, name='to_watch_show_list'),
    path('to_watch/shows/update/<int:pk>/', to_watch_show_update, name='to_watch_show_update'),
    path('to_watch/shows/delete/<int:pk>/', to_watch_show_delete, name='to_watch_show_delete'),

    # To Watch Movie URLs
    path('to_watch/movies/', to_watch_movie_list, name='to_watch_movie_list'),
    path('to_watch/movies/update/<int:pk>/', to_watch_movie_update, name='to_watch_movie_update'),
    path('to_watch/movies/delete/<int:pk>/', to_watch_movie_delete, name='to_watch_movie_delete'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Custom login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Optional
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)