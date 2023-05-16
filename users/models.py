from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Address(models.Model):
    # 우편번호, 도로명주소, 상세주소 필드 따로 두었음
    post_code = models.CharField(max_length=10)
    road_address = models.CharField(max_length=255)
    detail_address = models.CharField(max_length=255)

# 우리프로젝트 유저 필드 : 이름 아이디 성별 생년월일 비밀번호 휴대폰번호 주소(우편번호 + 주소) 이메일
class UserManager(BaseUserManager):
    def create_user(self, user_id, name, gender, birth, phone_number, email, address=None, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError('User must have an email address')
        
        if not user_id:
            raise ValueError('User must have an User ID')

        # Address 데이터 생성
        # address = Address.objects.create(postal_code=post_code, road_address=road_address, detail_address=detail_address)
        
        user = self.model(
            user_id=user_id,
            name=name,
            gender=gender,
            birth=birth,
            phone_number=phone_number,
            address=address,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, name, gender, birth, phone_number, email, address=None, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        # Address 데이터 생성
        # address = Address.objects.create(postal_code=post_code, road_address=road_address, detail_address=detail_address)

        user = self.create_user(
            user_id=user_id,
            password=password,
            name=name,
            gender=gender,
            birth=birth,
            phone_number=phone_number,
            address=address,
            email = self.normalize_email(email),
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    objects = UserManager()

    user_id = models.CharField(
        max_length=30,
        unique=True,
    )
    name = models.CharField(
        max_length=30,
        unique=True,
    )

    gender = models.CharField(
        max_length=10, 
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES[0][0],
        )

    birth = models.DateField(    
        null=True,
        blank=True,
   )
    
    # 폰번호 유효성 검사 추가
    phoneNumberRegex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')

    phone_number = models.CharField(
        validators = [phoneNumberRegex], 
        max_length = 11, 
        unique = True,
        )

    address = models.OneToOneField(
        Address, 
        on_delete=models.CASCADE,
        )

    email = models.EmailField(
        max_length=30,
        unique=True,
    )


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(
        default=timezone.now
    )

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['email', 'name', 'gender', 'phone_number', 'birth'] #필수로 받아야 되는 필드

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = _('Full name')



