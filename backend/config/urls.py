from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tickets/', include("tickets.api_urls")),   # API routes
    path("",include("tickets.page_urls")),  # Page routes
    path('',lambda r: __import__('django.shortcuts', fromlist=['redirect']).redirect('/tickets/')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)