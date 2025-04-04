from django.db import models

# Create your models here.
# payments/models.py


class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.username

class Business(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    business_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.transaction_id

class Notification(models.Model):
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message[:20]  # Display first 20 chars

