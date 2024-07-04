from .cart import Cart


def cart(request):
    """
    Процессор контекста корзины
    """

    return {'cart': Cart(request)}
