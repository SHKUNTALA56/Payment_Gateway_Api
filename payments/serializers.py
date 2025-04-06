from rest_framework import serializers
from .models import User, Business, Transaction, Notification



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Add necessary fields
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Assuming create_user is defined in User model
        return user



class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email','phone_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email','phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True},
                        'phone_number': {'required': True}
                        }


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'owner', 'business_name', 'business_email', 'business_phone', 'created_at']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'receiver', 'amount', 'transaction_type', 'timestamp', 'status']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'created_at']
