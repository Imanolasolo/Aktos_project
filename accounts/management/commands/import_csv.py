import csv
import requests
from io import StringIO
from decimal import Decimal
from django.core.management.base import BaseCommand
from accounts.models import CollectionAgency, Client, Consumer, Account


class Command(BaseCommand):  # ⬅️ This class must be named `Command`
    help = 'Import account, client, agency, and consumer data from remote CSV URL'

    def add_arguments(self, parser):
        # Add a command-line argument for the CSV URL
        parser.add_argument('url', type=str, help='Public Google Drive CSV URL')

    def handle(self, *args, **options):
        file_url = options['url']
        self.stdout.write("Fetching CSV from URL...")

        # Handle Google Drive links by converting them to direct download links
        if "drive.google.com" in file_url:
            try:
                file_id = file_url.split("/d/")[1].split("/")[0]
                file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            except IndexError:
                self.stderr.write("Invalid Google Drive link format.")
                return

        # Fetch the CSV file from the provided URL
        response = requests.get(file_url)
        if response.status_code != 200:
            self.stderr.write("Failed to download CSV file.")
            return

        # Save the CSV file locally for debugging or future use
        local_filename = "downloaded_file.csv"
        with open(local_filename, "w", encoding="utf-8") as local_file:
            local_file.write(response.text)
        self.stdout.write(f"CSV file saved locally as {local_filename}")

        # Parse the CSV content
        csv_file = StringIO(response.text)
        reader = csv.DictReader(csv_file)
        print("Detected CSV Headers:", reader.fieldnames)

        # Create default agency and client if they don't exist
        agency, _ = CollectionAgency.objects.get_or_create(name="Default Agency")
        client, _ = Client.objects.get_or_create(name="Default Client", agency=agency)

        # Cache to avoid duplicate account creation
        accounts_cache = {}

        for row in reader:
            # Extract and clean data from each row
            account_id = row['client reference no'].strip()
            balance = Decimal(row['balance'].strip())
            status = row['status'].strip().lower()
            consumer_name = row['consumer name'].strip()

            # Only process rows with valid statuses
            if status not in ['in_collection', 'collected']:
                continue

            # Create or fetch the consumer
            consumer, _ = Consumer.objects.get_or_create(full_name=consumer_name)

            # Create or fetch the account and associate it with the consumer
            if account_id not in accounts_cache:
                account = Account.objects.create(
                    client=client,
                    balance=balance,
                    status=status
                )
                accounts_cache[account_id] = account
            else:
                account = accounts_cache[account_id]

            # Add the consumer to the account
            account.consumers.add(consumer)

        # Print success message after processing all rows
        self.stdout.write(self.style.SUCCESS("✅ CSV data imported successfully."))