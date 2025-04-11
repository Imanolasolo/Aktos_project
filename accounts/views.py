import csv  # For handling CSV file operations
from io import TextIOWrapper  # For handling file-like objects
from decimal import Decimal  # For precise decimal arithmetic
from django.db.models import Q  # For building complex queries
from django.http import JsonResponse  # For returning JSON responses
from django.views import View  # Base class for class-based views
from django.db import transaction  # For managing database transactions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # For pagination
from accounts.models import CollectionAgency, Client, Consumer, Account  # Importing models
from django.views.decorators.csrf import csrf_exempt  # For disabling CSRF protection
from django.utils.decorators import method_decorator  # For applying decorators to class-based views

class AccountListView(View):
    """
    Handles GET requests to list accounts with optional filters and pagination.
    """
    def get(self, request):
        # Get query parameters
        min_balance = request.GET.get('min_balance')  # Minimum balance filter
        max_balance = request.GET.get('max_balance')  # Maximum balance filter
        consumer_name = request.GET.get('consumer_name')  # Consumer name filter
        status = request.GET.get('status')  # Account status filter
        limit = int(request.GET.get('limit', 10))  # Default limit is 10
        offset = int(request.GET.get('offset', 0))  # Default offset is 0

        # Build the query
        filters = Q()  # Initialize an empty query
        if min_balance:
            filters &= Q(balance__gte=min_balance)  # Filter for minimum balance
        if max_balance:
            filters &= Q(balance__lte=max_balance)  # Filter for maximum balance
        if consumer_name:
            filters &= Q(consumers__full_name__icontains=consumer_name)  # Filter for consumer name
        if status:
            filters &= Q(status=status)  # Filter for account status

        # Query the database
        accounts = Account.objects.filter(filters).distinct()  # Fetch accounts matching filters

        # Paginate the results
        paginator = Paginator(accounts, limit)  # Create a paginator object
        try:
            accounts_page = paginator.page((offset // limit) + 1)  # Get the current page
        except (EmptyPage, PageNotAnInteger):
            accounts_page = []  # Return an empty list if the page is invalid

        # Serialize the data
        data = [
            {
                "id": account.id,
                "client": account.client.name,
                "balance": float(account.balance),
                "status": account.status,
                "consumers": [consumer.full_name for consumer in account.consumers.all()],
            }
            for account in accounts_page
        ]

        # Return the paginated and serialized data as JSON
        return JsonResponse({
            "results": data,
            "total": paginator.count,
            "page": (offset // limit) + 1,
            "total_pages": paginator.num_pages,
        })

@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF protection for this view
class UploadCSVView(View):
    """
    Handles GET requests to read and return the content of a CSV file as JSON.
    """
    def get(self, request):
        # Path to the downloaded CSV file
        csv_file_path = "downloaded_file.csv"

        try:
            # Read the CSV file
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)  # Read the CSV file as a dictionary
                data = [row for row in reader]  # Convert rows to a list of dictionaries

            # Return the content as JSON
            return JsonResponse({"data": data}, status=200)

        except FileNotFoundError:
            # Handle the case where the file is not found
            return JsonResponse({"error": "CSV file not found. Please ensure the file exists."}, status=404)
        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)
