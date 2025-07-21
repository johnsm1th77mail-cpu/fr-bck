from django.urls import path, include

urlpatterns = [
    path('contact/', include('api.v1.contact.urls')),  # Contact API routeları
    path('blog/', include('api.v1.blog.urls')),        # Blog API routeları
    path('project/', include('api.v1.project.urls')) # Portfolio Project routeları (əgər varsa)
]
