from django.db import models


class Payment(models.Model):

    first_name = models.CharField(
        "User First Name", max_length=20, blank=True, default='')
    last_name = models.CharField(
        "User Last Name", max_length=20, blank=True, default='')
    email = models.EmailField("User email", blank=True, default='')
    phone = models.CharField(
        "User contact", max_length=20, blank=True, default='')
    login_type = models.CharField(
        "Social Login Type", max_length=4, blank=True, default='')
    fest_id = models.IntegerField("Fest ID", blank=True, default='')
    event_id = models.IntegerField("Event ID", blank=True, default='')
    org_id = models.IntegerField("Organization ID", blank=True, default='')
    amount = models.DecimalField("Payment Amount", max_digits=19,
                                 decimal_places=10, blank=True, default='')
    transaction_id = models.CharField(
        "Transaction ID", max_length=200, blank=True, default='')
    ticket_id = models.CharField(
        "Ticket ID", max_length=200, blank=True, default='')
    INITIATE = 'I'
    SUCCESS = 'S'
    FAILED = 'F'
    status_choices = (
        (INITIATE, 'Initiate'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed')
    )
    status = models.CharField(
        max_length=4,
        choices=status_choices,
        blank=True,
        default='',
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transaction_id
