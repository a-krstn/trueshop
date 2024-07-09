from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from io import BytesIO
from celery import shared_task
import weasyprint

from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Отправка уведомления на email
    при успешной оплате заказа
    """

    order = Order.objects.get(id=order_id)

    # формирование письма
    subject = f'TrueShop - Счет #{order.id}'
    message = 'Пожалуйста, ознакомьтесь со счетом Вашей покупки'
    email = EmailMessage(subject,
                         message,
                         'al-krstn@yandex.ru',
                         [order.email])

    # сгенерировать PDF
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out,
                                           stylesheets=stylesheets)

    # прикрепить pdf-файл
    email.attach(f'order_{order.id}.pdf',
                 out.getvalue(),
                 'application/pdf')

    # отправить письмо
    email.send()
