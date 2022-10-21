from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User

import pyotp

from .serializers import UserSerializer, SignUpSerializer, LoginUserSerializer
from .permissions import IsAdminOrSuperUser


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, )
    search_fields = ('username',)

    '''def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)'''

class SignUpView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():  # пользователь - новый.
            if serializer.validated_data['username'] == 'me':

                return Response(
                    {'error':'Нельзя создать пользователя "me" !'},
                    status=status.HTTP_400_BAD_REQUEST)

            otp = pyotp.random_base32()
            email = serializer.validated_data['email']
            serializer.validated_data['otp'] = otp
            serializer.save() # сохраняем пользователя
            self.send_mail(otp, email)
        else:
            try:  # пользователь - существует
                if (serializer.errors.get('username')[0].code == 'unique'
                    and serializer.errors.get('email')[0].code == 'unique'):

                    username = serializer.data['username']
                    email = serializer.data['email']
                    _existence_user = User.objects.get(username=username, email=email)
                    otp = pyotp.random_base32()
                    _existence_user.otp = otp
                    _existence_user.save()
                    self.send_mail(otp, email)
                else:

                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except:

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def send_mail(self, otp, email):
        """
        Template for sending mail
        """
        return send_mail('Токен OTP',
                         f'Для получения API-токена используйте следующий confirmation_code: {otp}',
                         'from@admin.com',
                         [email])


class LoginUserApiView(APIView):

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data # Fetch the data form serializer

        user = get_object_or_404(User, username=data['username'])

        if user.otp == data['confirmation_code']:
            # Generate Token
            refresh = RefreshToken.for_user(user)
            
            return Response(
            {
                'token': str(refresh.access_token),
            }
            , status=status.HTTP_200_OK
            )
        return Response(
            {
                'detail': 'Incorrect username or password',
            }
            , status=status.HTTP_400_BAD_REQUEST
            )
