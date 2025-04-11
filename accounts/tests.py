from django.test import TestCase
from accounts.models import Account, Client, Consumer, CollectionAgency
from decimal import Decimal

class AccountListViewTests(TestCase):
    def setUp(self):
        # Create test data for CollectionAgency, Client, Consumers, and Accounts
        agency = CollectionAgency.objects.create(name="Test Agency")
        client = Client.objects.create(name="Test Client", agency=agency)
        consumer1 = Consumer.objects.create(full_name="John Doe")
        consumer2 = Consumer.objects.create(full_name="Jane Smith")
        account1 = Account.objects.create(client=client, balance=Decimal("500.00"), status="in_collection")
        account2 = Account.objects.create(client=client, balance=Decimal("1500.00"), status="collected")
        account1.consumers.add(consumer1)
        account2.consumers.add(consumer2)

    def test_filter_by_min_balance(self):
        # Test filtering accounts by a minimum balance
        response = self.client.get('/accounts?min_balance=1000')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_filter_by_consumer_name(self):
        # Test filtering accounts by a consumer's name
        response = self.client.get('/accounts?consumer_name=john')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
