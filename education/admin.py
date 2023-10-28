from django.contrib import admin

from education.models import Payments


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'amount', 'payment_method',)
