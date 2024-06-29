from django.shortcuts import render
from django.views import generic

from services import services
from .models import Category, Product


class ProductList(generic.ListView):
    """
    Вывод списка всех продуктов или по категории
    """

    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    # paginate_by = 3

    def get_queryset(self):
        if self.kwargs.get('category_slug'):
            return services.filter_objects(Product.objects,
                                           category__slug=self.kwargs.get('category_slug'),
                                           available=True)
        return services.filter_objects(Product.objects,
                                       available=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = None
        if self.kwargs.get('category_slug'):
            category = services.get_instance_by_unique_field(Category, slug=self.kwargs.get('category_slug'))
            context['title'] = f'Категория: {category.name}'
            context['category'] = category
            context['categories'] = services.all_objects(Category.objects)
            return context
        context['title'] = 'Все товары'
        context['category'] = category
        context['categories'] = services.all_objects(Category.objects)
        return context


class ProductDetail(generic.DetailView):
    """
    Детальный вывод продукта
    """

    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context


