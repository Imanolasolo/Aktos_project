import csv
from io import TextIOWrapper
from decimal import Decimal
from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import CollectionAgency, Client, Consumer, Account


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


class UploadCSVView(View):
    def post(self, request):
        # Check if a file is provided
        csv_file = request.FILES.get('file')
        if not csv_file:
            return JsonResponse({"error": "No file provided"}, status=400)

        # Parse the CSV file
        try:
            csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(csv_data)
        except Exception as e:
            return JsonResponse({"error": f"Invalid CSV file: {str(e)}"}, status=400)

        # Create default agency & client
        agency, _ = CollectionAgency.objects.get_or_create(name="Default Agency")
        client, _ = Client.objects.get_or_create(name="Default Client", agency=agency)

        accounts_cache = {}

        # Process the CSV rows
        with transaction.atomic():  # Ensure atomicity
            for row in reader:
                account_id = row['client reference no'].strip()
                balance = Decimal(row['balance'].strip())
                status = row['status'].strip().lower()
                consumer_name = row['consumer name'].strip()

                # Only accept known statuses
                if status not in ['in_collection', 'collected']:
                    continue

                consumer, _ = Consumer.objects.get_or_create(full_name=consumer_name)

                if account_id not in accounts_cache:
                    account = Account.objects.create(
                        client=client,
                        balance=balance,
                        status=status
                    )
                    accounts_cache[account_id] = account
                else:
                    account = accounts_cache[account_id]

                account.consumers.add(consumer)

        return JsonResponse({"message": "CSV data imported successfully"}, status=201)