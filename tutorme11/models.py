from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission

from django.utils import timezone
from datetime import timedelta

from django.db import IntegrityError

from decimal import Decimal

class Class(models.Model):
    unique_id = models.PositiveIntegerField(unique=True, null=True, blank=True)  # Add this line
    subject = models.CharField(max_length=10)
    catalog_nbr = models.CharField(max_length=10)
    descr = models.CharField(max_length=100)

    class Meta:
        unique_together = ('subject', 'catalog_nbr')

    def save(self, *args, **kwargs):
        # If the unique_id is not set, generate a new one
        if not self.unique_id:
            max_id = Class.objects.all().aggregate(models.Max('unique_id'))['unique_id__max'] or 0
            self.unique_id = max_id + 1

            # Save the instance with the new unique_id
            try:
                super(Class, self).save(*args, **kwargs)
            except IntegrityError:
                # In case of a collision, skip
                pass
                # self.unique_id += 1
                # self.save(*args, **kwargs)
        else:
            super(Class, self).save(*args, **kwargs)

    def __str__(self):
        return self.subject + " " + self.catalog_nbr + " " + self.descr

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('tutor', 'Tutor'),
        ('tutoree', 'Tutoree'),
    )
    user_type = models.CharField(max_length=7, choices=USER_TYPE_CHOICES, blank=True, null=True)
    classes = models.ManyToManyField(Class, related_name="custom_users")
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='custom_users',
        verbose_name=('groups'),
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='custom_users',
        verbose_name=('user permissions'),
        help_text=('Specific permissions for this user.'),
        related_query_name='custom_user',
    )



class Tutorme_User(models.Model):
    is_student = models.BooleanField(default=True)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    enrolled_classes = models.ManyToManyField(Class, related_name='tutorme_users')
    venmo_username = models.CharField(max_length=50, null=True, blank=True, default="pgzdq")

    rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),null=True)

    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.username + " " + self.name + " " + str(self.is_student) + " " + str(self.rate)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_classes = models.TextField(blank=True, null=True)


class Request(models.Model):
    student_username = models.CharField(max_length=50)
    tutor_username = models.CharField(max_length=50)

    NO_RESPONSE = 'No Response'
    ACCEPTED = 'Accepted'
    REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (NO_RESPONSE, 'No Response'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default=NO_RESPONSE,
    )

    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.student_username + " to " + self.tutor_username + " with status " + self.status + " at " + str(self.time)
