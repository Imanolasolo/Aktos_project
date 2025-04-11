from django.urls import path
from .views import AccountListView, UploadCSVView

urlpatterns = [
    path('accounts', AccountListView.as_view(), name='accounts-list'),
    path('upload-csv', UploadCSVView.as_view(), name='upload-csv'),
]