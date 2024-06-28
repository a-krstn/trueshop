from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .utils import *


@only_objects_decorator
@prefetch_related_objects_decorator
@select_related_objects_decorator
def all_objects(objects: Manager, count: int = None) -> QuerySet:
    """Возвращает все объекты"""

    if count is None:
        return objects.all()
    return objects.all()[:count]


@only_objects_decorator
@prefetch_related_objects_decorator
@select_related_objects_decorator
def filter_objects(objects: Manager, **kwargs) -> QuerySet:
    """Возвращает отфильтрованные объекты"""

    return objects.filter(**kwargs)


def get_instance_by_unique_field(model, **kwargs):
    """Возвращает объект из БД по уникальному полю"""

    return get_object_or_404(model, **kwargs)
