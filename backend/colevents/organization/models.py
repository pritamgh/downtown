from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from user.models import CustomUser


fs = FileSystemStorage(location=settings.MEDIA_URL)


class Organization(models.Model):
    """ Model for organization """

    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True, related_name='organization_profile')
    type = models.CharField("organization type", max_length=20, default='')
    org_category = models.CharField(
        "organization category", max_length=20, default='')
    name = models.CharField("organization name", max_length=20, default='')
    address = models.TextField("organization address", default='')
    image = models.ImageField("organization image", storage=fs, blank=True)
    description = models.TextField(
        "organization description", max_length=120, default='')
    website = models.URLField()

    """ Main Co-ordinator """
    main_coordinator_name = models.CharField(
        "main Co-ordinator name", max_length=20, default='')
    main_coordinator_phone = models.CharField(
        "main Co-ordinator contact", max_length=20, default='')
    main_coordinator_email = models.EmailField(
        "main Co-ordinator email", default='')

    """ Sub Co-ordinator """
    sub_coordinator_name = models.CharField(
        "sub Co-ordinator name", max_length=20, default='')
    sub_coordinator_phone = models.CharField(
        "sub Co-ordinator contact", max_length=20, default='')
    sub_coordinator_email = models.EmailField(
        "sub Co-ordinator email", default='')

    """ Event/Team Manager """
    team = models.CharField("event/team name", max_length=20, default='')
    manager_name = models.CharField(
        "event/team manager name", max_length=20, default='')
    manager_phone = models.CharField(
        "event/team manager contact", max_length=20, default='')

    organization_delete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'organizer'
        verbose_name_plural = 'organizers'

    def __str__(self):
        return self.name


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):

    if instance.is_organization:
        Organization.objects.get_or_create(user=instance)
        token, created = Token.objects.get_or_create(user=instance)
        print(token.key)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):

    if instance.is_organization:
        instance.organization_profile.save()
