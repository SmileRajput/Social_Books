from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import date
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # Custom Fields
    name = models.CharField(max_length=50, default='anonymous')
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    public_visibility = models.BooleanField(default=False)
    birth_year = models.IntegerField(null=True, blank=True)

    # Override groups and permissions with unique related names
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    # Remove username field and use email instead
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # 'name' is required along with email for superusers # noqa

    # Link the custom user manager
    objects = CustomUserManager()

    # Calculate age based on birth year
    @property
    def age(self):
        if self.birth_year:
            current_year = date.today().year
            return current_year - self.birth_year
        return None

    def __str__(self):
        return self.email


class UploadedFiles(models.Model):
    VISIBILITY_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
    ]

    file = models.FileField(upload_to='uploads/', blank=False, null=False)
    title = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    visibility = models.CharField(max_length=7, choices=VISIBILITY_CHOICES, default='PUBLIC') # noqa
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    year_published = models.IntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
