from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    is_normaluser = models.BooleanField(default=True)
    is_organization = models.BooleanField(default=True)


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, null=True, related_name='user_profile')

    GOOGLE = 'G'
    FACEBOOK = 'F'
    social_auth_login_choices = (
        (GOOGLE, 'Google'),
        (FACEBOOK, 'Facebook'),
    )
    social_auth_login_type = models.CharField(
        max_length=4,
        choices=social_auth_login_choices,
        blank=True,
        default='',
    )
    fest_liked = models.ManyToManyField(
        'fest.Fest', blank=True, related_name='fest_liked')

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        if self.user.first_name:
            return '{self.user.first_name} {self.user.last_name}'.format(
                self=self).strip()
        return self.user.email


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):

    if instance.is_normaluser:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):

    if instance.is_normaluser:
        instance.user_profile.save()
