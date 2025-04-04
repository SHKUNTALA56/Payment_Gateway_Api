# payments/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BusinessViewSet, TransactionViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
