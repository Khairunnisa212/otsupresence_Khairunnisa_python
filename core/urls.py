from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('api/', include('employees.api_urls')),
    path('api/', include('attendance.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
