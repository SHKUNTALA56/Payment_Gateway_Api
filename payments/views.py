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
from .permissions import IsAdminUser, IsBusinessOwner, IsCustomer  # Import custom permissions
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreateSerializer, UserRegistrationSerializer
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema





#Create User
class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Adjust if needed
    

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully!", "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})    


# User ViewSet with JWT authentication and IsAuthenticated permission

class RegisterAPIView(APIView):

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# User ViewSet with JWT authentication and IsAuthenticated permission

class AdminOnlyView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users

    def get(self, request, *args, **kwargs):
        return Response({"message": "Public access for now"})
    
class BusinessOwnerView(APIView):
    permission_classes = [IsBusinessOwner]  # Business owner-only access

    def get(self, request, *args, **kwargs):
        # Logic for business owners
        return Response({"message": "This is a business owner-only view!"})

class CustomerOnlyView(APIView):
    permission_classes = [IsCustomer]  # Customer-only access

    def get(self, request, *args, **kwargs):
        # Logic for customer-specific data
        return Response({"message": "This is a customer-only view!"})   

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users can view

# Business ViewSet with JWT authentication and IsAuthenticated permission
class SomeView(APIView):
    permission_classes = [IsBusinessOwner]  # Only business owners can view

class SomeProtectedView(APIView):
    permission_classes = [IsBusinessOwner]  # Only business owners can view

    def get(self, request):
        return Response({"message": "Success!"})
    
class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsBusinessOwner]  # Only business owners can view

# Transaction ViewSet with JWT authentication and IsAuthenticated permission
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users can access

# Notification ViewSet with JWT authentication and IsAuthenticated permission
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Only authenticated users

# --- Webhook Handler ---
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])  # Open for everyone to access
def mpesa_webhook(request):
    try:
        data = request.data
        print("Webhook Payload:", data)
        return Response({"message": "Webhook received"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)  

# Home page view (can be accessed by anyone)
class HomePageView(TemplateView):
    template_name = 'home.html'  

# List and Detail views for Users (Admin only)
class UserListView(APIView):
    permission_classes = [IsAdminUser]  # Admin-only access

    def get(self, request):
        # Your logic here
        return Response({"users": []})

class UserDetailView(DetailView):
    model = User
    template_name = "user_detail.html"    

# Business List view (Admin or Business Owner access)
class BusinessListView(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAdminUser,IsBusinessOwner]  # Admin or Business Owner access

class BusinessDetailView(DetailView):
    model = Business
    template_name = 'business_detail.html'    

# Notification views (Admin or Business Owner access)
class NotificationListView(ListView):
    model = Notification
    template_name = 'notification_list.html'
    context_object_name = 'notifications'   

class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'notification_detail.html'
    context_object_name = 'notification'    

# Transaction views (Admin or Business Owner access)
class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

class TransactionDetailView(DetailView):
    model = Transaction
    template_name = 'transaction_detail.html'
    context_object_name = 'transaction'    

# Customer views (Admin or Customer access)
class IsCustomerListView(ListView):
    permission_required = 'payments.view_IsCustomer' 
    model = IsCustomer
    template_name = 'is_customer_list.html'
    context_object_name = 'customers'
    

class IsCustomerDetailView(DetailView):
    model = IsCustomer
    template_name = 'is_customer_detail.html'
    context_object_name = 'customer'        

# Webhook Handler (for testing purposes)
def webhook_handler(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            print(payload)
            return JsonResponse({'status': 'success', 'message': 'Webhook received successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failed', 'message': 'Invalid JSON payload'}, status=400)
    return JsonResponse({'status': 'failed', 'message': 'Invalid request method'}, status=400)

@swagger_auto_schema(
    method='get',
    operation_description="Get something",
    security=[{'Bearer': []}]
)
@api_view(['GET'])
@permission_classes([AllowAny])
def my_view(request):
    return Response({"msg": "You are authenticated"})
