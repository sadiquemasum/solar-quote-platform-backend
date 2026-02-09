from django.contrib import admin
from .models import Quote

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "monthly_bill", "monthly_savings", "created_at")
