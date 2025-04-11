from django.db import models

# Represents a collection agency that manages clients and their accounts
class CollectionAgency(models.Model):
    name = models.CharField(max_length=255)  # Name of the collection agency

    def __str__(self):
        return self.name


# Represents a client associated with a collection agency
class Client(models.Model):
    name = models.CharField(max_length=255)  # Name of the client
    agency = models.ForeignKey(
        CollectionAgency, 
        on_delete=models.CASCADE, 
        related_name='clients'  # Allows reverse lookup from CollectionAgency to its clients
    )

    def __str__(self):
        return self.name


# Represents a consumer who is associated with accounts
class Consumer(models.Model):
    full_name = models.CharField(max_length=255)  # Full name of the consumer

    def __str__(self):
        return self.full_name


# Represents an account associated with a client and one or more consumers
class Account(models.Model):
    STATUS_CHOICES = [
        ('in_collection', 'In Collection'),  # Account is currently in collection
        ('collected', 'Collected'),         # Account has been collected
    ]

    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE, 
        related_name='accounts'  # Allows reverse lookup from Client to its accounts
    )
    consumers = models.ManyToManyField(
        Consumer, 
        related_name='accounts'  # Allows reverse lookup from Consumer to their accounts
    )
    balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2  # Represents the balance amount in the account
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES  # Status of the account
    )

    def __str__(self):
        return f"Account {self.pk} for {self.client.name}"
