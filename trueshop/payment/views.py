import stripe
from decimal import Decimal

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.views import View

from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


class PaymentProcessView(View):
    """
    Представление оформления платежа
    """

    def get(self, request):
        order_id = request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        return render(request, 'payment/process.html', locals())

    def post(self, request):
        order_id = request.session.get('order_id', None)
        order = get_object_or_404(Order, id=order_id)
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        # добавление товарных позиций заказа в сеанс платежа
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'rub',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        # создание сеанса оформления платежа
        session = stripe.checkout.Session.create(**session_data)
        # перенаправление к платежной форме Stripe
        return redirect(session.url, code=303)


def payment_completed(request):
    """
    Представление успешного платежа
    """

    return render(request, 'payment/completed.html')


def payment_canceled(request):
    """
    Представление отмененного платежа
    """

    return render(request, 'payment/canceled.html')
