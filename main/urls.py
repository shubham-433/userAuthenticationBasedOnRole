
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from froala_editor import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('',include('appointment.urls')),
    path('froala_editor/',include('froala_editor.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

