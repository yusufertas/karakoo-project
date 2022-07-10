from django.core.mail import send_mail
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from customer.models import Customer, User, CustomerContact


@receiver(post_save, sender=CustomerContact)
def send_customer_email(sender, instance, created, **kwargs):
    if created:
        send_mail('Url which contains the registration link',
                  "Please register through this link",
                  instance.user.email,
                  [instance.email],
                  fail_silently=False)
