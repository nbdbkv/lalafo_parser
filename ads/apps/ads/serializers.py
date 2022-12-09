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
    images = ImageListSerializer(many=True)

    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'description', 'price', 'city', 'category', 'thumbnail_link', 'images', 'phone', 'author',
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        images = validated_data.pop('images')
        ad = Ad.objects.create(**validated_data)
        for image in images:
            Image.objects.create(ad=ad, **image)
        return ad

class AdDetailSerializer(serializers.ModelSerializer):
    images = ImageListSerializer(many=True)

    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'description', 'price', 'city', 'category', 'thumbnail_link', 'images', 'phone', 'author',
        )
