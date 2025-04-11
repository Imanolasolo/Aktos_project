from django.urls import path  # Importing path to define URL patterns
from .views import AccountListView, UploadCSVView  # Importing views for handling requests

# Defining URL patterns for the accounts app
urlpatterns = [
    path('accounts', AccountListView.as_view(), name='accounts-list'),  # URL for listing accounts
    path('upload-csv', UploadCSVView.as_view(), name='upload-csv'),  # URL for uploading CSV files
]