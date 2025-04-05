from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from payments import views  # Correct import
from payments.views import HomePageView 

# Redirect root URL to HomePageView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('payments.urls')),  # Include app's urls.py


     # Registration & Login page   
    path('api/auth/register/', views.register_user, name='register-api'),  # Add this line



    # Root path for the home page
    path('', HomePageView.as_view(), name='home'),

    # JWT Auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Your views for users, businesses, etc.
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('businesses/', views.BusinessListView.as_view(), name='business-list'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),

    # Role-based views
    path('admin-only/', views.AdminOnlyView.as_view(), name='admin-only'),
    path('business-owner-only/', views.BusinessOwnerView.as_view(), name='business-owner-only'),
    path('customer-only/', views.CustomerOnlyView.as_view(), name='customer-only'),
]
