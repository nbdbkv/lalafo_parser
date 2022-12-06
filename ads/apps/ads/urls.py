from django.urls import path

from .views import CategoryListView, AdsByCategoryView, AdDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('categories/<int:category_pk>/', AdsByCategoryView.as_view()),
    path('categories/<int:category_pk>/ads/<int:ad_pk>/', AdDetailView.as_view()),
]
