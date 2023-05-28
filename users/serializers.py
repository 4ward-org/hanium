from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from .models import User, UserManager, Address

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


# user_id, name, gender, birth, phone_number, email, address, password=None
class RegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    
    name = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    password2 = serializers.CharField(write_only=True, required=True)

    gender = serializers.ChoiceField(
        required=True,
        choices=GENDER_CHOICES,
    )


    class Meta:
        model = User
        fields = ('user_id', 'name', 'password',
                  'password2', 'gender', 'phone_number', 'address', 'birth', 'email')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "비밀번호가 다릅니다!"})

        return data

    def create(self, validated_data):
        address_data = validated_data['address']
        # address 정보를 post받는 serializer
        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)
        address = address_serializer.save()

        user = User.objects.create_user(
            user_id=validated_data['user_id'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            phone_number=validated_data['phone_number'],
            birth=validated_data['birth'],
            email=validated_data['email'],
            address=address,
        )

        # Address.objects.create(user=user, **address)

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
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            result = {
                'token': token,
                # 'name': user.name,
            }
            return result
        raise serializers.ValidationError(
            {"error": "Unable to log in with provided credentials."})


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name",)

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ("nickname", "university")
#         # extra_kwargs = {"image": {"required": False, "allow_null": True}}