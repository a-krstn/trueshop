from django.db.models import Manager


def only_objects_decorator(func: callable) -> callable:
    """Позволяет функциям, обращающимся к БД, принимать параметр only"""

    def only_objects_wrapper(objects: Manager, only=(), *args, **kwargs) -> callable:
        return func(objects, *args, **kwargs).only(*only)

    return only_objects_wrapper


def select_related_objects_decorator(func: callable) -> callable:
    """Позволяет функциям, обращающимся к БД, принимать параметр select_related"""

    def select_related_objects_wrapper(objects, select_related=(), *args, **kwargs) -> callable:
        return func(objects, *args, **kwargs).select_related(*select_related)

    return select_related_objects_wrapper


def prefetch_related_objects_decorator(func: callable) -> callable:
    """Позволяет функциям, обращающимся к БД, принимать параметр prefetch_related"""

    def prefetch_related_objects_wrapper(objects, prefetch_related=(), *args, **kwargs) -> callable:
        return func(objects, *args, **kwargs).prefetch_related(*prefetch_related)

    return prefetch_related_objects_wrapper
