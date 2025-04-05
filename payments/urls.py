# payments/urls.py
from django.http import HttpResponse
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BusinessViewSet, TransactionViewSet, mpesa_webhook, NotificationViewSet, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomerOnlyView 
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth.views import LoginView
from .views import RegisterAPIView





router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'notifications', NotificationViewSet)



def home(request):
    return HttpResponse("Welcome to the Payment Gateway!")



urlpatterns = [
    path('', include(router.urls)),  # This will handle API routes like /users/, /businesses/, etc.
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    
    #Customer-related ednpoints
    path('customer-only/', views.CustomerOnlyView.as_view(), name='customer-only'),


    # Business-related endpoints
    path('businesses/', views.BusinessListView.as_view(), name='business-list'),
    path('businesses/<int:pk>/', views.BusinessDetailView.as_view(), name='business-detail'),

    # Notification-related endpoints
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),

    # Transaction-related endpoints
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),

    # Customer-related endpoints
    path('is_customers/', views.IsCustomerListView.as_view(), name='is_customer_list'),
    path('is_customers/<int:pk>/', views.IsCustomerDetailView.as_view(), name='is_customer_detail'),

    # Webhook endpoint (POST requests only)
     path('webhook/', views.webhook_handler, name='webhook-handler'),

      # JWT Auth
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 

    # Login & Register endpoints

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('api/auth/register/', RegisterAPIView.as_view(), name='register-api'),


]



