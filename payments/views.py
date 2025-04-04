from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from .models import User, Business, Transaction, Notification
from .serializers import UserSerializer, BusinessSerializer, TransactionSerializer, NotificationSerializer
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework.generics import ListAPIView
from .models import User, Business
from django.http import JsonResponse
import json
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

# --- Webhook Handler ---
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # You may protect it with signature validation instead
def mpesa_webhook(request):
    try:
        data = request.data
        print("Webhook Payload:", data)
        return Response({"message": "Webhook received"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)  


class HomePageView(TemplateView):
    template_name = 'home.html'

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
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            print(payload)
            return JsonResponse({'status': 'success', 'message': 'Webhook received successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Invalid JSON payload'}, status=400)
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)