from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
			email=self.normalize_email(email),
			username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.type = 'DISPATCHER'
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default = False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Types(models.TextChoices):
        USER = "USER", "User"
        DISPATCHER = "DISPATCHER", "Dispatcher"
        DEPARTMENT_HEAD = "DEPARTMENT_HEAD", "Department_head"
        EXECUTOR = "EXECUTOR", "Executor"

    base_type = Types.USER
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    # class Meta:
    # indexes = [models.Index(fields=['fieldname1', 'fieldname1']), ]

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if not self.id:
            self.type = self.base_type
        return super().save(*args, **kwargs)

class UserManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Account.Types.USER)

class User(Account):
    base_type = Account.Types.USER
    objects = UserManager()

    class Meta:
        proxy = True

    def whisper(self):
        return "i'm user"


class DispatcherManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Account.Types.DISPATCHER)

class Dispatcher(Account):
    base_type = Account.Types.DISPATCHER
    objects = DispatcherManager()

    class Meta:
        proxy = True

    def whisper(self):
        return "i'm dispatcher"


class DepartmentHeadManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Account.Types.DEPARTMENT_HEAD)

class DepartmentHead(Account):
    base_type = Account.Types.DEPARTMENT_HEAD
    objects = DepartmentHeadManager()

    class Meta:
        proxy = True

    def whisper(self):
        return "i'm department head"


class ExecutorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=Account.Types.EXECUTOR)

class Executor(Account):
    base_type = Account.Types.EXECUTOR
    objects = ExecutorManager()

    class Meta:
        proxy = True

    def whisper(self):
        return "i'm executor"

# class ExecutorMore(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     gadgets = models.TextField()
