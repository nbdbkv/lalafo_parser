from django.contrib import admin

from .models import Category, Ad, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    ordering = ('id',)


class AdImageInline(admin.TabularInline):
    model = Image
    extra = 1


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'price', 'city', 'category', 'thumbnail_link', 'phone', 'author')
    inlines = (AdImageInline,)
    ordering = ('id',)
