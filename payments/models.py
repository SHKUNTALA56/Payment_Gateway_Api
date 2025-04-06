from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

AUTH_USER_MODEL = 'payments.User'

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager for the User model, providing helper methods for creating users and superusers.

    Methods:
        create_user: Creates a regular user with the specified email, password, and phone number.
        create_superuser: Creates a superuser with admin privileges.
    """
    def create_user(self, username, email, password=None, phone_number=None, **extra_fields):
        """
        Creates and saves a regular user with the given email, password, and phone number.

        Args:
            username (str): The username for the user.
            email (str): The email for the user.
            password (str): The password for the user (hashed).
            phone_number (str, optional): The phone number for the user.
            extra_fields (dict): Extra fields that will be added to the user model.

        Returns:
            User: The created user object.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, phone_number=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, password, and phone number.

        Args:
            username (str): The username for the superuser.
            email (str): The email for the superuser.
            password (str): The password for the superuser (hashed).
            phone_number (str, optional): The phone number for the superuser.
            extra_fields (dict): Extra fields to set for the superuser.

        Returns:
            User: The created superuser object.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, phone_number, **extra_fields)


class User(AbstractUser):
    """
    Custom user model for handling different user roles and extending default user attributes.

    Attributes:
        phone_number (str): The phone number of the user.
        role (str): The role of the user, can be 'admin', 'customer', or 'business_owner'.
    
    Methods:
        __str__: Returns the username of the user.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('business_owner', 'Business Owner'),
    ]
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')

    # Reverse accessor naming conflict solution
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set_custom',  # Specify custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_permissions_custom',  # Specify custom related name
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        """
        Returns the username of the user.

        Returns:
            str: The username of the user.
        """
        return self.username


class Business(models.Model):
    """
    Model representing a business entity in the system.

    Attributes:
        owner (User): The user who owns the business.
        business_name (str): The name of the business.
        business_email (str): The email of the business.
        business_phone (str): The phone number of the business.
        created_at (datetime): The timestamp when the business was created.

    Methods:
        __str__: Returns the business name.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200)
    business_email = models.EmailField(default='default@email.com')
    business_phone = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the name of the business.

        Returns:
            str: The business name.
        """
        return self.business_name


class Transaction(models.Model):
    """
    Model representing a financial transaction between two users.

    Attributes:
        sender (User): The user sending the money.
        receiver (User): The user receiving the money.
        amount (Decimal): The amount of money involved in the transaction.
        transaction_type (str): The type of transaction, either 'credit' or 'debit'.
        status (str): The status of the transaction, can be 'pending', 'completed', or 'failed'.
        timestamp (datetime): The timestamp when the transaction was created.

    Methods:
        __str__: Returns a string representation of the transaction (sender -> receiver: amount).
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=50, choices=[('credit', 'Credit'), ('debit', 'Debit')])
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the transaction, including sender, receiver, and amount.

        Returns:
            str: A formatted string representing the transaction.
        """
        return f"{self.sender} -> {self.receiver}: {self.amount}"


class Notification(models.Model):
    """
    Model representing a notification for a user.

    Attributes:
        user (User): The user to whom the notification is directed.
        message (str): The content of the notification.
        is_read (bool): Flag indicating whether the notification has been read.
        created_at (datetime): The timestamp when the notification was created.

    Methods:
        __str__: Returns the first 20 characters of the message.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the first 20 characters of the message.

        Returns:
            str: The first 20 characters of the notification message.
        """
        return self.message[:20]
