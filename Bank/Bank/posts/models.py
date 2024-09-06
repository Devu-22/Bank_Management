from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True)
    ACCOUNT_TYPE_CHOICES = [
        ('S', 'Savings'),
        ('C', 'Current'),
    ]
    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPE_CHOICES)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.user} - {self.account_type} "

class Transaction(models.Model):
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    TRANSACTION_TYPE_CHOICES = [
        ('D', 'Deposit'),
        ('W', 'Withdrawal'),
    ]
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_date = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return f"{self.account} - {self.transaction_type} of {self.amount} on {self.transaction_date}"