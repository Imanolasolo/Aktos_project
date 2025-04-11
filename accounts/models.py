from django.db import models

from django.db import models

class CollectionAgency(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=255)
    agency = models.ForeignKey(CollectionAgency, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return self.name


class Consumer(models.Model):
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Account(models.Model):
    STATUS_CHOICES = [
        ('in_collection', 'In Collection'),
        ('collected', 'Collected'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='accounts')
    consumers = models.ManyToManyField(Consumer, related_name='accounts')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Account {self.pk} for {self.client.name}"
