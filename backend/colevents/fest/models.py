from django.db import models
from organization.models import Organization


class Event(models.Model):

    event_name = models.CharField("event name", max_length=20, default='')
    event_rules = models.TextField("event rules")
    ticket_price = models.DecimalField("ticket price", max_digits=19,
                                       decimal_places=10, default='')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.event_name


class Sponsor(models.Model):

    sponsor_name = models.CharField(
        "event sponsor name", max_length=20, blank=True, null=True, default='')
    sponsor_picture = models.TextField(blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sponsor_name


class Fest(models.Model):
    """ Model for organization """

    organizer = models.ForeignKey(
        Organization, default='', on_delete=models.CASCADE)
    name = models.CharField("fest name", max_length=20, default='')
    image = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    website = models.URLField(blank=True, null=True, default='')
    social_media_pages = models.URLField(blank=True, null=True, default='')
    promo_video = models.TextField(blank=True, null=True)
    promo_video_thumbnail = models.TextField(blank=True, null=True,
                                             help_text='An image thumbnail.')

    events = models.ManyToManyField(Event, related_name='fest_events')
    sponsor = models.ManyToManyField(
        Sponsor, blank=True, related_name='fest_sponsor')

    """ Fest Manager """
    manager_name = models.CharField(
        "primary manager name", max_length=20, default='')
    manager_phone = models.CharField(
        "primary manager contact", max_length=20, default='')
    manager_email = models.EmailField("primary manager email", default='')

    sec_manager_name = models.CharField(
        "secondary manager name", max_length=20, default='')
    sec_manager_phone = models.CharField(
        "secondary manager contact", max_length=20, default='')

    """ Account Details of Manager for Payment """
    account_holder_name = models.CharField(
        "account holder name", max_length=20, default='')
    account_number = models.CharField(
        "account number", max_length=50, default='')
    IFSC = models.CharField("IFSC code", max_length=50, default='')

    total_likes = models.IntegerField("total likes", blank=True, null=True)
    fest_delete = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
