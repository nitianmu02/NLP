from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('nlp/', include('nlp.urls')),
    path("admin/", admin.site.urls),
]
