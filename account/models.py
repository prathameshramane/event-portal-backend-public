from django.db import models
from django.contrib.auth.models import AbstractUser

# Auth Token
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# Create your models here.
YEAR_CHOICES = (
    ('FE', 'First Year'),
    ('SE', 'Second Year'),
    ('TE', 'Third Year'),
    ('BE', 'Fourth Year'),
)

BRANCH_CHOICES = (
    ('COMP', 'Computer'),
    ('IT', 'Information Technology'),
    ('EXTC', 'Electronics & Telecommunication'),
    ('CIVIL', 'Civil'),
    ('MECH', 'Mechanical'),
    ('INST', 'Instrumentation'),
    ('ASH', 'ASH Department'),
    ('AIDS', 'Artificial Inteligence & Data Science'),
    ('CSE/DS', 'Computer Science / Data Science')
)


class Account(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    year = models.CharField(max_length=3, choices=YEAR_CHOICES)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    username = models.CharField(max_length=150, unique=True)
    desk = models.BooleanField(default=False)
    event_head = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['name', 'email', 'phone']

    def __str__(self):
        return self.name
