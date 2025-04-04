from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import User, Business, Transaction, Notification
from .serializers import UserSerializer, BusinessSerializer, TransactionSerializer, NotificationSerializer
from django.views.generic import DetailView, ListView
from rest_framework.generics import ListAPIView
from .models import User, Business
from django.http import JsonResponse





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

class UserListView(APIView):
    def get(self, request):
        # your logic here
        return Response({"users": []})
    
class UserDetailView(DetailView):
    model = User
    template_name = "user_detail.html"     

class BusinessListView(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer    

class BusinessDetailView(DetailView):
    model = Business
    template_name = 'business_detail.html'   

class NotificationListView(ListView):
    model = Notification
    template_name = 'notification_list.html'  # Adjust as needed
    context_object_name = 'notifications'   

class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'notification_detail.html'  # Adjust this as needed
    context_object_name = 'notification'    

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transaction_detail.html'
    context_object_name = 'transaction'    

def webhook_handler(request):
    # Logic for handling the webhook request goes here
    return JsonResponse({"message": "Webhook received successfully"})    

