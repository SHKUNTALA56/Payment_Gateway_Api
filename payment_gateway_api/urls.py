from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from payments import views  # Correct import
from payments.views import HomePageView 
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny



# Create a schema view with the permission set to allow any user to access
schema_view = get_schema_view(
    openapi.Info(
        title="Payment Gateway API",
        default_version='v1',
        description="API documentation for the payment gateway service",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@paymentgateway.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)
          # Redirect root URL to HomePageView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('payments.urls')),  # Include app's urls.py

          #  View Documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 


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
