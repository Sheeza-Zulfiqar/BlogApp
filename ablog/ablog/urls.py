"""ablog URL Configuration

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
from django.urls import path,include
from rest_framework import routers
from theblog import views
# from api.views import CommentViewSet
from api.views import RegistrationApiView
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

router = routers.SimpleRouter()
# router.register(r'posts', views.PostViewSet)
# router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('theblog.urls')),
    path('api/v1/',include('api.urls')),
    # path('api/v2/',include(router.urls)),
    # django authenticaion  system and it has lot of pkgz in urls that take care of urls so login logout register page
    # path('members/',include('django.contrib.auth.urls')),
    # path('members/',include('members.urls')),
    # path('myadmin/',include('manager.urls')),
    path('api_auth/',include('rest_framework.urls',
                            namespace='rest_framework')),
    path('auth/registerapi/', RegistrationApiView.as_view(), name='registerapi'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='refreshtoken'),
]
