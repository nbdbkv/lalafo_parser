from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


from .models import Category, Ad
from .serializers import CategoryListSerializer, AdsByCategorySerializer, AdDetailSerializer


class CategoryListView(ListCreateAPIView):
    """Отображение и добавление категорий"""
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class AdsByCategoryView(ListCreateAPIView):
    """Отображение и добавление объявлений по категориям"""
    serializer_class = AdsByCategorySerializer
    lookup_url_kwarg = 'category_pk'

    def get_queryset(self):
        return Ad.objects.filter(category_id=self.kwargs['category_pk']).prefetch_related('images')


class AdDetailView(RetrieveAPIView):
    """Отображение деталей объявления"""
    serializer_class = AdDetailSerializer
    lookup_url_kwarg = 'ad_pk'

    def get_queryset(self):
        return Ad.objects.filter(category_id=self.kwargs['category_pk'])
