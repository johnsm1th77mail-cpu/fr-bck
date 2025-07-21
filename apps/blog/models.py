from django.db import models
import re

def generate_slug(title):
    """Generate a slug from the title."""
    slug = title.lower()
    slug = re.sub(r'\s+', '-', slug)  # Replace spaces with hyphens
    slug = re.sub(r'[^\w-]+', '', slug)  # Remove non-alphanumeric characters except hyphens
    return slug.strip()

def upload_to(instance, filename):
    """Generate file path for uploaded images."""
    return f'blog/featured_images/{instance.slug}/{filename}'

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField(blank=True, null=True)
    featured_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    author = models.CharField(max_length=100)
    date = models.DateField()
    read_count = models.PositiveIntegerField(default=0)  # Tracks number of reads
    category = models.CharField(max_length=50)
    tags = models.JSONField()
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)  # New field for likes
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def save(self, *args, **kwargs):
        """Generate slug from title before saving."""
        if not self.slug:
            self.slug = generate_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogView(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField()
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'ip_address')
        verbose_name = 'Blog View'
        verbose_name_plural = 'Blog Views'

    def __str__(self):
        return f"{self.post.title} viewed by {self.ip_address}"

class BlogLike(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    ip_address = models.GenericIPAddressField()
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'ip_address')

    def __str__(self):
        return f"{self.post.title} - {self.ip_address}"
    