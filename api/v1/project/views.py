from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.project.models import Project, ProjectView, ProjectStar
from .serializers import ProjectSerializer
from django.utils import timezone

class ProjectListView(APIView):
    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectDetailView(APIView):
    def get(self, request, id, *args, **kwargs):
        try:
            project = Project.objects.get(id=id)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            
            if not ProjectView.objects.filter(project=project, ip_address=ip).exists():
                project.stats_views += 1
                project.save()
                ProjectView.objects.create(project=project, ip_address=ip, viewed_at=timezone.now())
            
            serializer = ProjectSerializer(project)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response(
                {'message': 'Project not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

class ProjectStarView(APIView):
    def post(self, request, id, *args, **kwargs):
        try:
            project = Project.objects.get(id=id)
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
            
            if ProjectStar.objects.filter(project=project, ip_address=ip).exists():
                return Response(
                    {'status': 'already_starred', 'stars_count': project.stats_stars},
                    status=status.HTTP_200_OK
                )
            
            project.stats_stars += 1
            project.save()
            ProjectStar.objects.create(project=project, ip_address=ip, starred_at=timezone.now())
            
            return Response(
                {'status': 'starred', 'stars_count': project.stats_stars},
                status=status.HTTP_200_OK
            )
        except Project.DoesNotExist:
            return Response(
                {'message': 'Project not found.'},
                status=status.HTTP_404_NOT_FOUND
            )