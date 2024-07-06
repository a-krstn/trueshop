from celery import shared_task
from django.core.mail import send_mail

from .models import Order


@shared_task
def order_created(order_id):
    """
    Отправки уведомления по электронной почте
    при успешном размещении заказа
    """

    order = Order.objects.get(id=order_id)
    subject = f'TrueShop Заказ №{order_id}'
    message = f'Уважаемый {order.first_name},\n\n' \
              f'Ваш заказ успешно размещен. ' \
              f'ID Вашего заказа - {order_id}.'
    mail_sent = send_mail(subject,
                          message,
                          'al-krstn@yandex.ru',
                          [order.email])
    return mail_sent
