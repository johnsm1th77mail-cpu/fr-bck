from rest_framework import serializers
from apps.blog.models import BlogPost
import json

class BlogPostSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'author', 'date', 'read_count', 'category', 'tags',
            'views_count', 'is_featured', 'likes_count'
        ]

    def validate_title(self, value):
        """Ensure title is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Title is required.")
        return value

    def validate_tags(self, value):
        """Ensure tags is a list of strings."""
        # Handle case where tags is a stringified JSON
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError("Tags must be a valid JSON list of strings.")
        
        if not isinstance(value, list) or not all(isinstance(tag, str) for tag in value):
            raise serializers.ValidationError("Tags must be a list of strings.")
        return value