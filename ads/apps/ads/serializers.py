from rest_framework import serializers

from .models import Category, Image, Ad


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_link',)


class AdsByCategorySerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    images = ImageListSerializer(many=True)
    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'description', 'price', 'city', 'category', 'thumbnail_link', 'images', 'phone', 'author',
        )


class AdDetailSerializer(serializers.ModelSerializer):
    images = ImageListSerializer(many=True)
    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'description', 'price', 'city', 'category', 'thumbnail_link', 'images', 'phone', 'author',
        )
