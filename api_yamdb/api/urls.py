from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)


urlpatterns = [
    #path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls)),
]
