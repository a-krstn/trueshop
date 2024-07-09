from django.contrib import admin
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.urls import reverse

import csv
import datetime

from .models import Order, OrderItem


def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=(obj.id,))
    return mark_safe(f'<a href="{url}">PDF</a>')


order_pdf.short_description = 'Счет'


def order_detail(obj):
    """
    Возвращает HTML-ссылку
    """

    url = reverse('orders:admin_order_detail', args=(obj.id,))
    return mark_safe(f'<a href="{url}">Просмотр</a>')


order_detail.short_description = 'Детали заказа'


def export_to_csv(modeladmin, request, queryset):
    """
    Административное действие для преобразования заказа в csv-файл
    """

    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not
              field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Экспортировать в CSV'


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
                    order_stripe_payment, 'created', 'updated',
                    order_detail, order_pdf)
    list_filter = ('paid', 'created', 'updated')
    inlines = (OrderItemInline,)
    actions = (export_to_csv,)



