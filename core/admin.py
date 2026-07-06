from django.contrib import admin
from .models import Movie, Genre

# Models ko admin mein register kar rahe hain
admin.site.register(Genre)
admin.site.register(Movie)