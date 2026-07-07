# from django.shortcuts import render,get_object_or_404
# from .models import Movie
#
#
# def home(request):
#     # Saari movies nikal rahe hain neeche list mein dikhane ke liye
#     movies = Movie.objects.all().order_by('-created_at')
#
#     # Yahan hum specially "The Dark Knight" ko search karke banner ke liye set kar rahe hain
#     featured_movie = Movie.objects.filter(title="The Dark Knight").first()
#
#     # Agar kisi wajah se The Dark Knight database mein na mile, toh list ki pehli movie dikha do
#     if not featured_movie:
#         featured_movie = movies.first()
#
#     return render(request, 'core/home.html', {
#         'movies': movies,
#         'featured_movie': featured_movie
#     })
#
# def movie_detail(request, pk):
#     # pk (Primary Key) se specific movie ko database se nikal rahe hain
#     movie = get_object_or_404(Movie, pk=pk)
#     return render(request, 'core/movie_detail.html', {'movie': movie})


# import requests
# from django.shortcuts import render
#
# # TMDB API Configuration
# API_KEY = '5b6b88939c086d1b7a2d4b68e2114251' # Yeh ek test key hai, aap baad mein apni bana sakte ho
# BASE_URL = 'https://api.themoviedb.org/3'
# IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/'
#
# def home(request):
#     # 1. API se Trending Movies mangwa rahe hain
#     trending_url = f"{BASE_URL}/trending/movie/week?api_key={API_KEY}"
#     response = requests.get(trending_url)
#     data = response.json()
#     movies = data.get('results', [])
#
#     # 2. Jo sabse pehli movie aayegi, usko Banner (Hero) banayenge
#     featured_movie = movies[0] if movies else None
#
#     # 3. Data ko HTML mein bhej rahe hain
#     return render(request, 'core/home.html', {
#         'movies': movies,
#         'featured_movie': featured_movie,
#         'image_base_url': IMAGE_BASE_URL, # Images ka base URL bhej rahe hain
#     })
#
# def movie_detail(request, pk):
#     # API se ek specific movie ki poori detail mangwa rahe hain (Trailer ke sath)
#     detail_url = f"{BASE_URL}/movie/{pk}?api_key={API_KEY}&append_to_response=videos"
#     response = requests.get(detail_url)
#     movie = response.json()
#
#     # Trailer ka YouTube key nikal rahe hain
#     trailer_key = None
#     if 'videos' in movie and 'results' in movie['videos']:
#         for video in movie['videos']['results']:
#             if video['type'] == 'Trailer' and video['site'] == 'YouTube':
#                 trailer_key = video['key']
#                 break
#
#     return render(request, 'core/movie_detail.html', {
#         'movie': movie,
#         'trailer_key': trailer_key,
#         'image_base_url': IMAGE_BASE_URL,
#     })


import requests
from django.conf import settings
from django.shortcuts import render
from users.models import Watchlist

def fetch_tmdb_data(endpoint):
    url = f"{settings.TMDB_BASE_URL}{endpoint}"
    try:
        response = requests.get(url, verify=False, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


# def home(request):
#     # 1. URL se Page aur Genre uthayenge (Default: Page 1, No Genre)
#     page = int(request.GET.get('page', 1))
#     genre_id = request.GET.get('genre', '')
#
#     # 2. Agar koi genre select hai toh 'Discover' API use karenge, nahi toh 'Trending'
#     if genre_id:
#         endpoint = f"/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}&page={page}"
#     else:
#         endpoint = f"/trending/movie/week?api_key={settings.TMDB_API_KEY}&page={page}"
#
#     data = fetch_tmdb_data(endpoint)
#     movies = data.get('results', []) if data else []
#
#     # Banner ke liye humesha Trending ki pehli movie rakhenge (Looks Better)
#     banner_data = fetch_tmdb_data(f"/trending/movie/week?api_key={settings.TMDB_API_KEY}")
#     featured_movie = banner_data.get('results', [None])[0] if banner_data else None
#
#     # 3. Context mein sab kuch bhejenge taaki HTML ko pata chale hum kahan hain
#     return render(request, 'core/home.html', {
#         'featured_movie': featured_movie,
#         'movies': movies,
#         'current_page': page,
#         'next_page': page + 1,
#         'prev_page': page - 1 if page > 1 else None,
#         'current_genre': genre_id,
#         'image_base_url': settings.TMDB_IMAGE_URL,
#     })


def home(request):
    # 1. URL se Page aur Genre uthayenge (Default: Page 1, No Genre)
    page = int(request.GET.get('page', 1))
    genre_id = request.GET.get('genre', '')

    # 2. Agar koi genre select hai toh 'Discover' API use karenge, nahi toh 'Trending'
    if genre_id:
        endpoint = f"/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres={genre_id}&page={page}"
    else:
        endpoint = f"/trending/movie/week?api_key={settings.TMDB_API_KEY}&page={page}"

    data = fetch_tmdb_data(endpoint)
    movies = data.get('results', []) if data else []

    # 🔴 SUPER FIX 1: Har movie ke andar ek safe 'display_title' bana rahe hain
    for m in movies:
        m['display_title'] = m.get('title') or m.get('name') or "Unknown"

    # Banner ke liye humesha Trending ki pehli movie rakhenge (Looks Better)
    banner_data = fetch_tmdb_data(f"/trending/movie/week?api_key={settings.TMDB_API_KEY}")

    # Yahan ek chota sa fix: [None] ki jagah [{}] taaki object safe rahe
    featured_movie = banner_data.get('results', [{}])[0] if banner_data else None

    # 🔴 SUPER FIX 2: Banner wali movie ke liye bhi 'display_title' add kar rahe hain
    if featured_movie:
        featured_movie['display_title'] = featured_movie.get('title') or featured_movie.get('name') or "Unknown"

    # 3. Context mein sab kuch bhejenge taaki HTML ko pata chale hum kahan hain
    return render(request, 'core/home.html', {
        'featured_movie': featured_movie,
        'movies': movies,
        'current_page': page,
        'next_page': page + 1,
        'prev_page': page - 1 if page > 1 else None,
        'current_genre': genre_id,
        'image_base_url': settings.TMDB_IMAGE_URL,
        'is_tv': False,  # Yeh flag batayega ki hum Movies par hain, Series par nahi
    })

# def search(request):
#     query = request.GET.get('q')
#     search_results = []
#
#     if query:
#         endpoint = f"/search/movie?api_key={settings.TMDB_API_KEY}&query={query}"
#         data = fetch_tmdb_data(endpoint)
#         if data and 'results' in data:
#             search_results = data['results']
#
#     return render(request, 'core/search.html', {
#         'movies': search_results,
#         'query': query,
#         'image_base_url': settings.TMDB_IMAGE_URL,
#     })


# def movie_detail(request, pk):
#     # 1. Main Movie Detail + Videos + Credits (Actors) + Recommendations
#     endpoint = f"/movie/{pk}?api_key={settings.TMDB_API_KEY}&append_to_response=videos,credits,recommendations"
#     movie = fetch_tmdb_data(endpoint)
#
#     context = {
#         'movie': movie,
#         'image_base_url': settings.TMDB_IMAGE_URL,
#     }
#
#     if movie:
#         # Actors ki list (top 6 actors)
#         context['cast'] = movie.get('credits', {}).get('cast', [])[:6]
#         # Milti julti movies
#         context['recommended_movies'] = movie.get('recommendations', {}).get('results', [])[:6]
#
#     return render(request, 'core/movie_detail.html', context)

def search(request):
    query = request.GET.get('q')
    results_list = [] # Name changed to avoid confusion
    if query:
        endpoint = f"/search/multi?api_key={settings.TMDB_API_KEY}&query={query}"
        data = fetch_tmdb_data(endpoint)
        results_list = data.get('results', []) if data else []

        for item in results_list:
            item['display_title'] = item.get('title') or item.get('name') or "Unknown"
            # Yeh backend par hi check kar lega ki TV hai ya Movie
            item['is_tv_result'] = item.get('media_type') == 'tv'

    return render(request, 'core/search.html', {
        'movies': results_list, # Template ke 'if movies' se match karne ke liye
        'query': query,
        'image_base_url': settings.TMDB_IMAGE_URL,
    })

def movie_detail(request, pk):
    # 1. Main Movie Detail + Videos + Credits (Actors) + Recommendations
    endpoint = f"/movie/{pk}?api_key={settings.TMDB_API_KEY}&append_to_response=videos,credits,recommendations"
    movie = fetch_tmdb_data(endpoint)

    context = {
        'movie': movie,
        'image_base_url': settings.TMDB_IMAGE_URL,
        'trailer_key': None  # Trailer ke liye default khali rakha hai
    }

    if movie:
        # Actors ki list (top 6 actors)
        context['cast'] = movie.get('credits', {}).get('cast', [])[:6]
        # Milti julti movies
        context['recommended_movies'] = movie.get('recommendations', {}).get('results', [])[:6]

        # 2. YAHAN HAI TRAILER DHOONDHNE KA LOGIC
        if 'videos' in movie and 'results' in movie['videos']:
            in_watchlist = False
            if request.user.is_authenticated:
                from users.models import Watchlist
                in_watchlist = Watchlist.objects.filter(
                    user=request.user,
                    tmdb_id=pk,
                    media_type='movie'
                ).exists()

            context['in_watchlist'] = in_watchlist
            for video in movie['videos']['results']:
                # Official YouTube trailer dhoondho
                if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                    context['trailer_key'] = video['key']
                    break

            # Agar official trailer na mile, toh jo bhi pehli video ho wo utha lo
            if not context['trailer_key'] and movie['videos']['results']:
                context['trailer_key'] = movie['videos']['results'][0]['key']


    return render(request, 'core/movie_detail.html', context)


def tv_home(request):
    page = int(request.GET.get('page', 1))

    # TV Shows ka trending data
    endpoint = f"/trending/tv/week?api_key={settings.TMDB_API_KEY}&page={page}"
    data = fetch_tmdb_data(endpoint)
    tv_shows = data.get('results', []) if data else []

    # Banner ke liye pehla TV show
    banner_data = fetch_tmdb_data(f"/trending/tv/week?api_key={settings.TMDB_API_KEY}")
    featured_tv = banner_data.get('results', [None])[0] if banner_data else None

    # Hum same home.html use karenge, bas data TV ka bhejenge
    return render(request, 'core/home.html', {
        'featured_movie': featured_tv,  # Template mein same variable name chalega
        'movies': tv_shows,  # TV shows ki list
        'current_page': page,
        'next_page': page + 1,
        'prev_page': page - 1 if page > 1 else None,
        'image_base_url': settings.TMDB_IMAGE_URL,
        'is_tv': True  # Yeh flag HTML ko batayega ki hum TV page par hain
    })


def tv_detail(request, pk):
    # TV Show ki details (Seasons ke sath)
    endpoint = f"/tv/{pk}?api_key={settings.TMDB_API_KEY}&append_to_response=videos,credits,recommendations"
    tv_show = fetch_tmdb_data(endpoint)

    context = {
        'movie': tv_show,  # Reusing variable name
        'image_base_url': settings.TMDB_IMAGE_URL,
        'trailer_key': None,
        'is_tv': True
    }

    if tv_show:
        context['cast'] = tv_show.get('credits', {}).get('cast', [])[:6]
        context['recommended_movies'] = tv_show.get('recommendations', {}).get('results', [])[:6]

        # Trailer dhoondhna
        if 'videos' in tv_show and 'results' in tv_show['videos']:
            for video in tv_show['videos']['results']:
                if video['type'] == 'Trailer' and video['site'] == 'YouTube':
                    context['trailer_key'] = video['key']
                    break

    # TV ke liye hume ek naya HTML page banana padega jisme Seasons/Episodes hon
    return render(request, 'core/tv_detail.html', context)


def anime_home(request):
    """Placeholder view for Anime section."""
    # We will implement this later. For now, show a blank page or reuse home style.
    # Reusing home template structure but filtering TMDB by 'Animation' genre (ID 16).

    page = int(request.GET.get('page', 1))
    # TMDB Animation genre ID is 16.
    endpoint = f"/discover/movie?api_key={settings.TMDB_API_KEY}&with_genres=16&page={page}"
    data = fetch_tmdb_data(endpoint)
    results = data.get('results', []) if data else []
    for item in results:
        item['display_title'] = item.get('title') or item.get('name') or "Unknown"
        item['is_tv_result'] = False  # conceptual listing as movie-style

    # Banner as default trending (keep it simple)
    banner_data = fetch_tmdb_data(f"/trending/movie/week?api_key={settings.TMDB_API_KEY}")
    featured_movie = banner_data.get('results', [{}])[0] if banner_data else None
    if featured_movie:
        featured_movie['display_title'] = featured_movie.get('title') or featured_movie.get('name') or "Unknown"

    return render(request, 'core/home.html', {
        'featured_movie': featured_movie,
        'movies': results,
        'current_page': page,
        'next_page': page + 1,
        'prev_page': page - 1 if page > 1 else None,
        'current_genre': '16',  # Force Animation genre ID
        'image_base_url': settings.TMDB_IMAGE_URL,
        'is_tv': False,  # conceptual movies
        'page_type': 'anime',  # Flag to know it's anime page
    })


def actor_movies(request, actor_id):
    """
    Ek specific actor (person) ki saari movies aur TV shows nikalta hai TMDB API se.
    """
    # 1. Actor ki details mangwao, aur sath mein unke movie_credits bhi (append_to_response se)
    endpoint = f"/person/{actor_id}?api_key={settings.TMDB_API_KEY}&append_to_response=movie_credits,tv_credits"
    actor_data = fetch_tmdb_data(endpoint)

    if not actor_data:
        # Agar actor data na mile toh kya karna hai, handle kar sakte ho (abhi empty page dikhayega)
        return render(request, 'core/actor_movies.html', {'error': 'Actor not found.'})

    actor_name = actor_data.get('name', 'Unknown Actor')

    # 2. Actor ke movie aur tv credits nikal lo
    movies = actor_data.get('movie_credits', {}).get('cast', [])
    tv_shows = actor_data.get('tv_credits', {}).get('cast', [])

    # Dono lists ko combine kar lo taaki saara content ek sath dikhe
    all_credits = movies + tv_shows

    # 3. Sirf wo filter karo jinke paas poster hai
    valid_credits = [c for c in all_credits if c.get('poster_path')]

    # 4. Filtered credits mein display_title aur type set karo (taaki search.html jaisa chal sake)
    for c in valid_credits:
        c['display_title'] = c.get('title') or c.get('name') or "Unknown"
        # Agar item TV show hai toh flag set karo (for correct URLs like detail views)
        c['is_tv_result'] = c.get('media_type') == 'tv' or 'first_air_date' in c

    # 5. Optional: Popularity ke hisab se sort kar do (zyada popular pehle)
    valid_credits = sorted(valid_credits, key=lambda x: x.get('popularity', 0), reverse=True)

    context = {
        'actor_name': actor_name,
        'movies': valid_credits,  # Variable 'movies' rakha hai for template consistency
        'image_base_url': settings.TMDB_IMAGE_URL,
    }

    return render(request, 'core/actor_movies.html', context)