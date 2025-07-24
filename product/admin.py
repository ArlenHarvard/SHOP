from django.contrib import admin
from .models import Category, City, District, Estate, Image

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_category')
    search_fields = ('title',)
    list_filter = ('parent_category',)

class CityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('title', 'city')
    list_filter = ('city',)
    search_fields = ('title',)

class EstateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'city', 'district', 'price', 'is_active', 'created_at')
    list_filter = ('category', 'city', 'district', 'is_active')
    search_fields = ('title', 'descriptions')
    ordering = ('-created_at',)
    list_editable = ('is_active',)
    list_per_page = 20

class ImageAdmin(admin.ModelAdmin):
    list_display = ('estate', 'image')

# Регистрация моделей
admin.site.register(Category, CategoryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Estate, EstateAdmin)
admin.site.register(Image, ImageAdmin)
