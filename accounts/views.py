import csv
from io import TextIOWrapper
from decimal import Decimal
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import CollectionAgency, Client, Consumer, Account
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class AccountListView(View):
    def get(self, request):
        # Get query parameters
        min_balance = request.GET.get('min_balance')
        max_balance = request.GET.get('max_balance')
        consumer_name = request.GET.get('consumer_name')
        status = request.GET.get('status')
        limit = int(request.GET.get('limit', 10))  # Default limit is 10
        offset = int(request.GET.get('offset', 0))  # Default offset is 0

        # Build the query
        filters = Q()
        if min_balance:
            filters &= Q(balance__gte=min_balance)
        if max_balance:
            filters &= Q(balance__lte=max_balance)
        if consumer_name:
            filters &= Q(consumers__full_name__icontains=consumer_name)
        if status:
            filters &= Q(status=status)

        # Query the database
        accounts = Account.objects.filter(filters).distinct()

        # Paginate the results
        paginator = Paginator(accounts, limit)
        try:
            accounts_page = paginator.page((offset // limit) + 1)
        except (EmptyPage, PageNotAnInteger):
            accounts_page = []

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

        return JsonResponse({
            "results": data,
            "total": paginator.count,
            "page": (offset // limit) + 1,
            "total_pages": paginator.num_pages,
        })

@method_decorator(csrf_exempt, name='dispatch')
class UploadCSVView(View):
    def get(self, request):
        # Path to the downloaded CSV file
        csv_file_path = "f:\\CODECODIX\\aktos_project\\downloaded_file.csv"

        try:
            # Read the CSV file
            with open(csv_file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]  # Convert rows to a list of dictionaries

            # Return the content as JSON
            return JsonResponse({"data": data}, status=200)

        except FileNotFoundError:
            return JsonResponse({"error": "CSV file not found. Please ensure the file exists."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)