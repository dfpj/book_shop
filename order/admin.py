from django.contrib import admin
from .models import Order,OrderItem


class OrderItemsInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('book',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','user','created','updated','paid')
    list_filter = ('created','paid')
    inlines = (OrderItemsInline,)


