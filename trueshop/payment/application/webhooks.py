from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import stripe

from orders.models import Order
from ..tasks import payment_completed


@csrf_exempt
def stripe_webhook(request):
    """
    Верификация подписи
    """

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        # Недопустимая полезная нагрузка
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Недопустимая подпись
        return HttpResponse(status=400)

    # проверка, что полученное событие является успешным оформлением платежа
    if event.type == 'checkout.session.completed':
        # извлечение сеансового объекта
        session = event.data.object
        print(session)
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExists:
                return HttpResponse(status=404)
            # пометка заказа как оплаченного
            order.paid = True
            order.stripe_id = session.payment_intent
            order.save()
            payment_completed.delay(order.id)

    return HttpResponse(status=200)
