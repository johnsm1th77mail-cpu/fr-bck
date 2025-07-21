from django.contrib import admin
from .models import Project, ProjectView, ProjectStar

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'stats_views', 'stats_stars', 'is_featured')
    search_fields = ('title', 'category', 'technologies')
    list_filter = ('category', 'is_featured')

@admin.register(ProjectView)
class ProjectViewAdmin(admin.ModelAdmin):
    list_display = ('project', 'ip_address', 'viewed_at')
    search_fields = ('project__title', 'ip_address')

@admin.register(ProjectStar)
class ProjectStarAdmin(admin.ModelAdmin):
    list_display = ('project', 'ip_address', 'starred_at')
    search_fields = ('project__title', 'ip_address')