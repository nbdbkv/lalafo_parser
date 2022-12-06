from rest_framework.generics import ListAPIView, RetrieveAPIView


from .models import Category, Ad
from .serializers import CategoryListSerializer, AdsByCategorySerializer, AdDetailSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class AdsByCategoryView(ListAPIView):
    serializer_class = AdsByCategorySerializer
    lookup_url_kwarg = 'category_pk'

    def get_queryset(self):
        return Ad.objects.filter(
            is_active=True,
            collection_id=self.kwargs['category_pk']
        ).prefetch_related('images')


class AdDetailView(RetrieveAPIView):
    serializer_class = AdDetailSerializer
    lookup_url_kwarg = 'ad_pk'

    def get_queryset(self):
        return Ad.objects.filter(
            is_active=True,
            collection_id=self.kwargs['category_pk']
        )
