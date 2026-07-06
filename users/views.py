from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from django.http import JsonResponse
from .models import Watchlist

def register(request):
    # Agar user ne form submit kiya hai (POST)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # User ko database mein save kar do
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! Ab aap login kar sakte hain.')
            return redirect('login')  # Account banne ke baad login page par bhej do
    else:
        # Agar user pehli baar page par aaya hai (GET)
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """PREMIUM Profile View withintegrated Watchlist display."""
    my_watchlist = Watchlist.objects.filter(user=request.user)

    return render(request, 'users/profile.html', {
        'watchlist': my_watchlist,
        'image_base_url': settings.TMDB_IMAGE_URL,
    })


@login_required
@require_POST
def add_to_watchlist(request):
    """Handle adding items to watchlist and redirect back."""
    tmdb_id = request.POST.get('tmdb_id')
    media_type = request.POST.get('media_type')
    title = request.POST.get('title')
    poster_path = request.POST.get('poster_path')

    # Movie ko save karo (agar pehle se nahi hai)
    Watchlist.objects.get_or_create(
        user=request.user,
        tmdb_id=tmdb_id,
        media_type=media_type,
        defaults={'title': title, 'poster_path': poster_path}
    )

    # 🔴 REDIRECT BACK (Highlight: Isse white page nahi aayega)
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
@require_POST
def remove_from_watchlist(request):
    """Handle removing items and redirect back."""
    tmdb_id = request.POST.get('tmdb_id')
    media_type = request.POST.get('media_type')

    # Delete entry
    Watchlist.objects.filter(user=request.user, tmdb_id=tmdb_id, media_type=media_type).delete()

    # 🔴 REDIRECT BACK (Wapas usi page par bhej do)
    return redirect(request.META.get('HTTP_REFERER', 'home'))