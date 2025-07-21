from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('<int:id>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('<int:id>/star/', views.ProjectStarView.as_view(), name='project-like'),
]