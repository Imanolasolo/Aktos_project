from django.contrib import admin
from django.urls import path, include

# Define the URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel for site administration
    path('', include('accounts.urls')),  # Route to the accounts app's URL configurations
]