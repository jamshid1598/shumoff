from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from sorl.thumbnail.admin import AdminImageMixin

from .models import (
    Category, 
    Product, 
    Images, 
)


# Register your models here.
class CategoryAdmin(AdminImageMixin, admin.ModelAdmin):
    lsit_display = ('category_name', 'primary', 'tools', 'accessory',)
    ordering = ('category_name', 'primary', 'tools', 'accessory',)
    search_fields = ('category_name', 'primary', 'tools', 'accessory',)

    fieldsets = (
        ('Категория', {
            "fields": (
                'category_name',
                'image',

                'primary', 
                'tools', 
                'accessory',
            ),
        }),
    )

admin.site.register(Category, CategoryAdmin)

class ProductImageAdmin(AdminImageMixin, admin.StackedInline):
    model   = Images
    extra   = 1
    max_num = 3
class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [ProductImageAdmin]
    
    list_display = ('category', 'name', 'price', 'discount', 'currency', 'quantity', 'published_at', 'updated_at', )
    list_display_links = ('name', 'published_at', 'updated_at', )
    search_fields = ('name', 'price', 'discount', 'currency', 'category', 'quantity', 'published_at', 'updated_at', )
    ordering = ('name', 'price', 'discount', 'currency', 'quantity', 'category', 'published_at', 'updated_at', )
    list_editable = ('price', 'discount', 'currency',  'category', 'quantity', )

    prepopulated_fields = {'slug': ('name', )}

    fieldsets = (
        ('Категория', {
            "fields": (
                ('category',)
            ),
        }),
        ('Товар', {
            "fields": (
                ('name', 'slug', 'description', 'price', 'discount', 'currency', 'quantity')
            ),
        }),
        ('Изображений', {
            "fields": (
                'image',
                'caption',
            ),
        }),
    )
    formfield_overrides = {
        models.TextField : {'widget' : TinyMCE}
    }
    
admin.site.register(Product, ProductAdmin)