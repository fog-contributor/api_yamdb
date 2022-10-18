from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from reviews.models import User, Role

from .serializers import UserSerializer
from .permissions import IsAdminOrSuperUser


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAdminOrSuperUser,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, )
    search_fields = ('user__username',)
