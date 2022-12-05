from django.contrib import admin

from .models import Category, Ad, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # ordering = ('id',)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'city', 'category', 'thumbnail_link', 'phone', 'author')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_link')
