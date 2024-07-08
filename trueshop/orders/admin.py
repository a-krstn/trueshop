from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


def order_stripe_payment(order_obj):
    """
    Возвращает ссылку на платеж Stripe
    """

    url = order_obj.get_stripe_url()
    if order_obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{order_obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


order_stripe_payment.short_description = 'Платеж Stripe'


class OrderItemInline(admin.TabularInline):
    """
    Класс вставляет модель OrderItem внутристрочно в модель Order
    """

    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_stripe_payment, 'created', 'updated')
    list_filter = ('paid', 'created', 'updated')
    inlines = (OrderItemInline,)
