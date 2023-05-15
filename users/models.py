from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, nickname, university, email, password=None):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not username:
            raise ValueError(_('Users must have an username'))

        user = self.model(
            username=username,
            nickname=nickname,
            university=university,
            email=email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, university, nickname, email, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            username=username,
            password=password,
            nickname=nickname,
            university=university,
            email=email
        )

        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


UNIVERSITY_CHOICES = (
    ('dongduk', '동덕여자대학교'),
    ('sungshin', '성신여자대학교'),
    ('soongsil', '숭실대학교'),
    ('hanyang', '한양대학교')
)


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    username = models.CharField(
        max_length=30,
        unique=True,
    )
    nickname = models.CharField(
        max_length=30,
        null=False,
        unique=True
    )

    university = models.CharField(
        max_length=40,
        choices=UNIVERSITY_CHOICES,
        default=UNIVERSITY_CHOICES[0][0]
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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'university', 'email'] #필수로 받아야 되는 필드

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)

    def __str__(self):
        return self.nickname

    def get_full_name(self):
        return self.nickname

    def get_short_name(self):
        return self.nickname

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All superusers are staff
        return self.is_superuser

    get_full_name.short_description = _('Full name')
