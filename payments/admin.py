from django.contrib import admin

# Register your models here.
from .models import User, Business, Transaction, Notification  # import your model(s)

# Register your model(s) with the admin interface
admin.site.register(User)
admin.site.register(Business)
admin.site.register(Transaction)
admin.site.register(Notification)

