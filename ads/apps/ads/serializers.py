from rest_framework import serializers

from .models import Category, Image, Ad


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'slug', 'name',)


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image_link',)


class AdsByCategorySerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ('title', 'price', 'city', 'thumbnail_link', 'phone', 'author')


class AdDetailSerializer(serializers.ModelSerializer):
    images = ImageListSerializer(many=True)
    class Meta:
        model = Ad
        fields = (
            'title', 'description', 'price', 'city', 'category', 'thumbnail_link', 'images', 'phone', 'author',
        )
