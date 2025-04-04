from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import User, Business, Transaction, Notification
from .serializers import UserSerializer, BusinessSerializer, TransactionSerializer, NotificationSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

@csrf_exempt
@api_view(['POST'])
def mpesa_webhook(request):
    # Handle webhook data here
    data = request.data
    # Process the webhook data and return appropriate response
    return Response({"message": "Webhook received"}, status=200)    

