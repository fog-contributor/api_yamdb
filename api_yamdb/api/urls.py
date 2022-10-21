from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet, SignUpView, LoginUserApiView

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', LoginUserApiView.as_view(),
         name='token_obtain_pair'),
    path('v1/', include(router_v1.urls)),
]
