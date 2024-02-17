from django.db import models
from django.core.validators import RegexValidator
from threading import Lock


class Seller(models.Model):
    username = models.CharField(max_length=20, unique=True)
    credit = models.DecimalField(max_digits=25, decimal_places=10)
    logs = models.TextField()

    def __str__(self):
        return self.username


class Costumer(models.Model):
    phone_number_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    phone_number = models.CharField(validators=[phone_number_regex], max_length=17, unique=True)
    credit = models.DecimalField(max_digits=25, decimal_places=10)
    logs = models.TextField()

    def __str__(self):
        return self.phone_number


class Transaction(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=25, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.username} to {self.costumer.phone_number}"


class RegistrationLog(models.Model):
    types = ['Seller Registration', 'Customer Registration']
    log_type = models.CharField(max_length=500)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None, null=True)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE, default=None, null=True)
    credit = models.DecimalField(default=None, null=True, max_digits=25, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.log_type


class TransactionLog(models.Model):
    types = ['Seller Increase', 'Transaction']
    log_type = models.CharField(max_length=500)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None, null=True)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE, default=None, null=True)
    amount = models.DecimalField(default=None, null=True, max_digits=25, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.log_type


class DeletionLog(models.Model):
    types = ['Seller Deletion', 'Customer deletion']
    log_type = models.CharField(max_length=500)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None, null=True)
    costumer = models.ForeignKey(Costumer, on_delete=models.CASCADE, default=None, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.log_type


class InnerCharge(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None, null=True)
    amount = models.DecimalField(default=None, null=True, max_digits=25 ,decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Charging {self.seller.username}"
