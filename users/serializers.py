from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import User, UserManager

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


UNIVERSITY_CHOICES = (
    ('dongduk', '동덕여자대학교'),
    ('sungshin', '성신여자대학교'),
    ('soongsil', '숭실대학교'),
    ('hanyang', '한양대학교')
)


class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    
    nickname = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    password2 = serializers.CharField(write_only=True, required=True)

    university = serializers.ChoiceField(
        required=True,
        choices=UNIVERSITY_CHOICES
    )

    class Meta:
        model = User
        fields = ('username', 'nickname', 'password',
                  'password2', 'university', 'email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 다릅니다!"})

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            nickname=validated_data['nickname'],
            university=validated_data['university'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        # token = Token.objects.create(user=user)
        
        message = render_to_string('users/authentication_email.html', {
            'user': user, # 생성한 사용자 객체
            'domain': '127.0.0.1:8000',  # 나중에 배포할 때 url 이름으로 변경
            # .decode('utf-8')
            'uid': urlsafe_base64_encode(force_bytes(user.pk)), # 암호화된 User pk
            'token': account_activation_token.make_token(user), # 생성한 사용자 객체를 통해 생성한 token 값
        })

        mail_subject = 'Complete your account registration'
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email]) # EmailMessage(제목,내용,받는이)
        email.send()

        return user
        


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            result = {
                'token': token,
                'nickname': user.nickname,
            }
            return result
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."})


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("nickname",)

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ("nickname", "university")
#         # extra_kwargs = {"image": {"required": False, "allow_null": True}}