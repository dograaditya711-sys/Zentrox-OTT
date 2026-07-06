from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# === USER PROFILE MODEL (Premium Features like watchlists) ===
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Automatically create profile when a User is created (Magic!)
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Automatically save profile when User is saved
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# === WATCHLIST MODEL (Tracks user's favorite content) ===
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')
    tmdb_id = models.IntegerField()
    media_type = models.CharField(max_length=10) # 'movie' or 'tv'
    title = models.CharField(max_length=255) # Cache the title for performance
    poster_path = models.CharField(max_length=255) # Cache poster path for performance
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-added_on']
        unique_together = ('user', 'tmdb_id', 'media_type') # Ensure no duplicates

    def __str__(self):
        return f'{self.user.username} - {self.title}'