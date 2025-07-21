from django.contrib import admin
from .models import BlogPost, BlogView, BlogLike

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'date', 'category', 'views_count', 'read_count', 'is_featured')
    list_filter = ('category', 'is_featured', 'date')
    search_fields = ('title', 'excerpt', 'content', 'author', 'tags')
    readonly_fields = ('slug', 'created_at', 'views_count', 'read_count')
    date_hierarchy = 'date'
    ordering = ('-date',)
    list_editable = ('is_featured',)

@admin.register(BlogView)
class BlogViewAdmin(admin.ModelAdmin):
    list_display = ('post', 'ip_address', 'viewed_at')
    list_filter = ('viewed_at',)
    search_fields = ('post__title', 'ip_address')
    date_hierarchy = 'viewed_at'
    ordering = ('-viewed_at',)

@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'ip_address', 'liked_at')
    search_fields = ('post__title', 'ip_address')