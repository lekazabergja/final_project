from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Loan, Cash_flow

admin.site.register(Loan)
admin.site.register(Cash_flow)

