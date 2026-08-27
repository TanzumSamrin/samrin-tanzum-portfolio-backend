from django.contrib import admin
from .models import Category, Tag, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'author', 'published_at', 'views_count', 'is_featured']
    search_fields = ['title', 'content']
    list_filter = ['status', 'category', 'tags', 'is_featured']
    readonly_fields = ['slug', 'views_count', 'reading_time', 'published_at']