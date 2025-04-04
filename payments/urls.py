# payments/urls.py

from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BusinessViewSet, TransactionViewSet, mpesa_webhook, NotificationViewSet, UserDetailView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'notifications', NotificationViewSet)






urlpatterns = [
    path('', include(router.urls)),
    path('webhook/', mpesa_webhook),

     path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),

    # Business-related endpoints
    path('businesses/', views.BusinessListView.as_view(), name='business-list'),
    path('businesses/<int:pk>/', views.BusinessDetailView.as_view(), name='business-detail'),

    # Notification-related endpoints
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', views.NotificationDetailView.as_view(), name='notification-detail'),

    # Transaction-related endpoints
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', views.TransactionDetailView.as_view(), name='transaction-detail'),

    # Webhook endpoint (POST requests only)
    path('webhook/', views.webhook_handler, name='webhook'),

]
