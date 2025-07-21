from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog-list'),
    path('<str:slug>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('<slug:slug>/like/', views.BlogLikeView.as_view(), name='blog-like'),
]