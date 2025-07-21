from django.db import models
from django.utils import timezone

def upload_to(instance, filename):
    return f'project/featured_images/{instance.id}/{filename}'

class Project(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    featured_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    technologies = models.JSONField(default=list)
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    year = models.CharField(max_length=4, blank=True)
    team_size = models.PositiveIntegerField(default=1)
    duration = models.CharField(max_length=50, blank=True)
    impact = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    stats_views = models.PositiveIntegerField(default=0)
    stats_stars = models.PositiveIntegerField(default=0)
    stats_forks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class ProjectView(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'ip_address')

    def __str__(self):
        return f"{self.project.title} - {self.ip_address}"

class ProjectStar(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stars')
    ip_address = models.GenericIPAddressField()
    starred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'ip_address')

    def __str__(self):
        return f"{self.project.title} - {self.ip_address}"