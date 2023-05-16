import traceback
# Create your views here.
from rest_framework import generics, status, permissions
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework.response import Response
from .models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.authtoken.models import Token
from django.shortcuts import redirect

from .serializers import RegisterSerializer, LoginSerializer

from .token import account_activation_token
from rest_framework.views import APIView


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        name = serializer.validated_data['name']
        return Response({"token": token.key,
                        "name": name},
                        status=status.HTTP_200_OK)


class UserActivate(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        try: 
            uid = force_str(urlsafe_base64_decode(uidb64)) # 암호화된 유저의 PK # .encode('utf-8')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                token = Token.objects.create(user=user)
                user.save()
                return HttpResponseRedirect('http://localhost:5173/auth-login.html') # 계정 활성화가 되면 바로 프론트엔드 login 페이지로
            
            else:
                return HttpResponseRedirect('http://localhost:5173/auth-register.html') # 만료된 링크를 타고 들어가면 다시 프론트엔드 회원가입 페이지로

        except Exception as e:
            print(traceback.format_exc())