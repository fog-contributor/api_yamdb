from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework import filters

import pyotp

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category, Comment, Genre, Title, Review
from .permissions import AuthorOrReadOnly
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    LoginUserSerializer,
    CategorySerializer, 
    CommentSerializer,
    GenreSerializer,
    TitleSerializer,
    TitlePostPatchSerializer,
    ReviewSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)


class SignUpView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():  # пользователь - новый.
            if serializer.validated_data['username'] == 'me':

                return Response(
                    {'error': 'Нельзя создать пользователя "me" !'},
                    status=status.HTTP_400_BAD_REQUEST)

            otp = pyotp.random_base32()
            email = serializer.validated_data['email']
            serializer.validated_data['otp'] = otp
            serializer.save()
            self.send_mail(otp, email)
        else:
            try:  # пользователь - существует
                if (serializer.errors.get('username')[0].code == 'unique' and
                        serializer.errors.get('email')[0].code == 'unique'):
                    username = serializer.data['username']
                    email = serializer.data['email']
                    _existence_user = User.objects.get(username=username,
                                                       email=email)
                    otp = pyotp.random_base32()
                    _existence_user.otp = otp
                    _existence_user.save()
                    self.send_mail(otp, email)
                else:

                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            except Exception:

                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_mail(self, otp, email):

        return send_mail('Токен OTP',
                         f'Для получения API-токена '
                         f'используйте следующий confirmation_code: {otp}',
                         'from@admin.com',
                         [email])


class LoginUserView(APIView):

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if user.otp == data['confirmation_code']:
            refresh = RefreshToken.for_user(user)

            return Response({'token': str(refresh.access_token), },
                            status=status.HTTP_200_OK)

        return Response({'detail': 'Incorrect username or password', },
                        status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):

    def get(self, request):
        me = get_object_or_404(User, username=request.user)
        serializer = UserSerializer(me)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        me = get_object_or_404(User, username=request.user)
        serializer = UserSerializer(me, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateListDel(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Кастомный класс для создания и удаления категорий и жанров."""
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateListDel):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related()
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)


class GenreViewSet(CreateListDel):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostPatchSerializer
        return TitleSerializer
        

class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.select_related()
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly,)
