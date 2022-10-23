from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Avg

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework import filters

import pyotp
from api.filters import TitleFilter

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category, Comment, Genre, Title, Review
from .permissions import AuthorOrReadOnly, IsAdminOrSuperUser, IsModeratorOrIsOwner, ReadOnly

from .serializers import (
    UserSerializer,
    SignUpSerializer,
    LoginUserSerializer,
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    TitleSerializer,
    TitlePostPatchSerializer,
    ReviewSerializer,
    CurrentUserSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdminOrSuperUser,)
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
                if (
                    serializer.errors.get('username')[0].code == 'unique'
                    and serializer.errors.get('email')[0].code == 'unique'
                ):
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
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if user.otp == data['confirmation_code']:
            refresh = RefreshToken.for_user(user)
            user.otp = None  # Удаляем ОТР после выдачи токена
            user.save()

            return Response({'token': str(refresh.access_token), },
                            status=status.HTTP_200_OK)

        return Response({'detail': 'Incorrect username or password', },
                        status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = (AuthorOrReadOnly,)

    def get(self, request):
        me = get_object_or_404(User, username=request.user)
        serializer = CurrentUserSerializer(me)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        me = get_object_or_404(User, username=request.user)
        serializer = CurrentUserSerializer(me, data=request.data, partial=True)
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
    permission_classes = (IsAdminOrSuperUser,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.select_related()
#     serializer_class = CommentSerializer
#     permission_classes = (IsModeratorOrIsOwner,)

    # Закоментил на время. После тестов если все ок, то можно удалить 
#     def get_permissions(self):
#         if self.action == 'create' or self.action == 'destroy':
#             return (IsAdminOrSuperUser(),)
#         return super().get_permissions()


class GenreViewSet(CreateListDel):
    permission_classes = (IsAdminOrSuperUser,)
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return (IsAdminOrSuperUser(),)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrSuperUser,)
    queryset = Title.objects.all()
#     queryset = (
#         Title.objects.all().annotate(Avg('reviews__score')).order_by('name')
#     )

    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return TitlePostPatchSerializer
        return TitleSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy' or self.action == 'partial_update':
            return (IsAdminOrSuperUser(),)
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    # permission_classes = (IsModeratorOrIsOwner,)

    permission_classes = (AuthorOrReadOnly,)

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        context.update({"title": title})
        return context

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)
        return title.reviews.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)

