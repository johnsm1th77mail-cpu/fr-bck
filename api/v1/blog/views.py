from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.blog.models import BlogPost, BlogView, BlogLike
from .serializers import BlogPostSerializer
from django.utils import timezone

class BlogListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BlogDetailView(APIView):
    def get(self, request, slug, *args, **kwargs):
        try:
            post = BlogPost.objects.get(slug=slug)
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            
            # Check if this IP has viewed this post
            if not BlogView.objects.filter(post=post, ip_address=ip).exists():
                # Increment views_count and read_count, and record the view
                post.views_count += 1
                post.read_count += 1
                post.save()
                BlogView.objects.create(post=post, ip_address=ip, viewed_at=timezone.now())
            
            serializer = BlogPostSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BlogPost.DoesNotExist:
            return Response(
                {'message': 'Blog post not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

class BlogLikeView(APIView):
    def post(self, request, slug, *args, **kwargs):
        try:
            post = BlogPost.objects.get(slug=slug)
            # Get client IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            
            # Check if this IP has liked this post
            if not BlogLike.objects.filter(post=post, ip_address=ip).exists():
                # Increment likes_count and record the like
                post.likes_count += 1
                post.save()
                BlogLike.objects.create(post=post, ip_address=ip, liked_at=timezone.now())
                return Response(
                    {
                        'status': 'liked',
                        'likes_count': post.likes_count
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {
                        'status': 'already_liked',
                        'likes_count': post.likes_count
                    },
                    status=status.HTTP_200_OK
                )
        except BlogPost.DoesNotExist:
            return Response(
                {'message': 'Blog post not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
            