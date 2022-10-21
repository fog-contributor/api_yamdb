from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import UserViewSet, SignUpView, LoginUserView, CurrentUserView

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view()),
    path('v1/auth/token/', LoginUserView.as_view()),
    path('v1/users/me/', CurrentUserView.as_view()),
    path('v1/', include(router_v1.urls)),
]
