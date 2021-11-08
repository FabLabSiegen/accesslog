"""accesslog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from utilities import views as v
from rest import views as r
from django.conf import settings
from django.conf.urls.static import static

#rest api
router = routers.DefaultRouter()
router.register(r'users', r.UserViewSet)
router.register(r'groups', r.GroupViewSet)
router.register(r'models', r.ThreeDimensionalModelViewSet, basename="ThreeDimensionalModel")
router.register(r'gcode', r.GCodeViewSet, basename="GCode")
router.register(r'slicingconfig', r.SlicingConfigViewSet, basename="SlicingConfig")
router.register(r'printjob', r.PrintJobViewSet, basename="PrintJob")
router.register(r'mediafile', r.PrintMediaFileViewSet, basename="PrintMediaFile")

#url routing
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', v.register, name="utilities"),
    path('manage/', v.MachineListView.as_view(), name="Machine-List"),
    path('', include('utilities.urls')),
    path('', include("django.contrib.auth.urls")),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/mediafiles/<int:pk>/', r.PrintMediaFileByPrintJob.as_view() , name="MediaFilesByPrintJob-get"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
