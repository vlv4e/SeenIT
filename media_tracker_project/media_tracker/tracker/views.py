from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Show, Movie, ToWatchShow, ToWatchMovie  # Import ToWatchShow and ToWatchMovie
from .forms import MovieForm, ShowForm, ToWatchShowForm, ToWatchMovieForm  # Import ToWatchShowForm and ToWatchMovieForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def log_show(request):
    if request.method == 'POST':
        title = request.POST['title']
        duration = request.POST['duration']
        Show.objects.create(title=title, duration=duration, user=request.user)
        return redirect('home')
    return render(request, 'tracker/log_show.html')

@login_required
def log_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        duration = request.POST['duration']
        Movie.objects.create(title=title, duration=duration, user=request.user)
        return redirect('home')
    return render(request, 'tracker/log_movie.html')

@login_required
def home(request):
    shows = Show.objects.filter(user=request.user)
    movies = Movie.objects.filter(user=request.user)

    total_time = sum(show.duration for show in shows) + sum(movie.duration for movie in movies)
    total_shows = shows.count()
    total_movies = movies.count()
    total_duration_shows = sum(show.duration for show in shows)
    total_duration_movies = sum(movie.duration for movie in movies)

    # Calculate daily stats
    daily_stats = {
        'dates': [],
        'movies': [],
        'shows': []
    }

    # Get the last 7 days
    today = timezone.now().date()
    for i in range(7):
        date = today - timezone.timedelta(days=i)
        daily_movies_count = movies.filter(watched_date=date).count()
        daily_shows_count = shows.filter(watched_date=date).count()

        daily_stats['dates'].append(date.strftime('%Y-%m-%d'))
        daily_stats['movies'].append(daily_movies_count)
        daily_stats['shows'].append(daily_shows_count)

    context = {
        'shows': shows,
        'movies': movies,
        'total_time': total_time,
        'total_shows': total_shows,
        'total_movies': total_movies,
        'total_duration_shows': total_duration_shows,
        'total_duration_movies': total_duration_movies,
        'daily_stats': daily_stats,
    }
    return render(request, 'tracker/home.html', context)

# Movie CRUD views
@login_required
def movie_list(request):
    movies = Movie.objects.filter(user=request.user)
    return render(request, 'tracker/movie_list.html', {'movies': movies})

@login_required
def movie_create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user  # Set the user
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'tracker/movie_form.html', {'form': form})

@login_required
def movie_update(request, pk):
    movie = get_object_or_404(Movie, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'tracker/movie_form.html', {'form': form})

@login_required
def movie_delete(request, pk):
    movie = get_object_or_404(Movie, pk=pk, user=request.user)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'tracker/movie_confirm_delete.html', {'movie': movie})

# Show CRUD views
@login_required
def show_list(request):
    shows = Show.objects.filter(user=request.user)
    return render(request, 'tracker/show_list.html', {'shows': shows})

@login_required
def show_create(request):
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            show = form.save(commit=False)
            show.user = request.user  # Set the user
            show.save()
            return redirect('show_list')
    else:
        form = ShowForm()
    return render(request, 'tracker/show_form.html', {'form': form})

@login_required
def show_update(request, pk):
    show = get_object_or_404(Show, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ShowForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            return redirect('show_list')
    else:
        form = ShowForm(instance=show)
    return render(request, 'tracker/show_form.html', {'form': form})

@login_required
def show_delete(request, pk):
    show = get_object_or_404(Show, pk=pk, user=request.user)
    if request.method == 'POST':
        show.delete()
        return redirect('show_list')
    return render(request, 'tracker/show_confirm_delete.html', {'show': show})


def show_list(request):
    shows = Show.objects.all()  # Get all shows by default
    return render(request, 'tracker/show_list.html', {'shows': shows})

def show_favorite_list(request):
    favorite_shows = Show.objects.filter(is_favorite=True)
    return render(request, 'tracker/show_favorite_list.html', {'shows': favorite_shows})

def show_favorite(request, pk):
    show = get_object_or_404(Show, pk=pk)
    show.is_favorite = not show.is_favorite
    show.save()
    return redirect('show_list')


def movie_favorite(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    movie.is_favorite = not movie.is_favorite
    movie.save()
    return redirect('movie_list')

def movie_favorite_list(request):
    favorite_movies = Movie.objects.filter(is_favorite=True)
    return render(request, 'tracker/movie_favorite_list.html', {'movies': favorite_movies})
# To Watch Show CRUD views
@login_required
def to_watch_show_list(request):
    to_watch_shows = ToWatchShow.objects.filter(user=request.user)
    form = ToWatchShowForm()  # Instantiate the form
    if request.method == 'POST':
        form = ToWatchShowForm(request.POST)
        if form.is_valid():
            to_watch_show = form.save(commit=False)
            to_watch_show.user = request.user
            to_watch_show.save()
            return redirect('to_watch_show_list')
    return render(request, 'tracker/to_watch_show_list.html', {'to_watch_shows': to_watch_shows, 'form': form})  # Pass the form to the template

@login_required
def to_watch_show_update(request, pk):
    to_watch_show = get_object_or_404(ToWatchShow, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ToWatchShowForm(request.POST, instance=to_watch_show)
        if form.is_valid():
            form.save()
            return redirect('to_watch_show_list')
    else:
        form = ToWatchShowForm(instance=to_watch_show)
    return render(request, 'tracker/to_watch_show_form.html', {'form': form, 'to_watch_show': to_watch_show})

@login_required
def to_watch_show_delete(request, pk):
    to_watch_show = get_object_or_404(ToWatchShow, pk=pk, user=request.user)
    if request.method == 'POST':
        to_watch_show.delete()
        return redirect('to_watch_show_list')
    return render(request, 'tracker/to_watch_show_confirm_delete.html', {'to_watch_show': to_watch_show})

# To Watch Movie CRUD views
@login_required
def to_watch_movie_list(request):
    to_watch_movies = ToWatchMovie.objects.filter(user=request.user)
    form = ToWatchMovieForm()  # Instantiate the form
    if request.method == 'POST':
        form = ToWatchMovieForm(request.POST)
        if form.is_valid():
            to_watch_movie = form.save(commit=False)
            to_watch_movie.user = request.user
            to_watch_movie.save()
            return redirect('to_watch_movie_list')
    return render(request, 'tracker/to_watch_movie_list.html', {'to_watch_movies': to_watch_movies, 'form': form})  # Pass the form to the template

@login_required
def to_watch_movie_update(request, pk):
    to_watch_movie = get_object_or_404(ToWatchMovie, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ToWatchMovieForm(request.POST, instance=to_watch_movie)
        if form.is_valid():
            form.save()
            return redirect('to_watch_movie_list')
    else:
        form = ToWatchMovieForm(instance=to_watch_movie)
    return render(request, 'tracker/to_watch_movie_form.html', {'form': form, 'to_watch_movie': to_watch_movie})

@login_required
def to_watch_movie_delete(request, pk):
    to_watch_movie = get_object_or_404(ToWatchMovie, pk=pk, user=request.user)
    if request.method == 'POST':
        to_watch_movie.delete()
        return redirect('to_watch_movie_list')
    return render(request, 'tracker/to_watch_movie_confirm_delete.html', {'to_watch_movie': to_watch_movie})