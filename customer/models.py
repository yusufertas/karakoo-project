from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    class Meta:
        db_table = 'auth_user'


class CustomerContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_contact')
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='customer_contact')
    first_name = models.CharField(max_length=256, db_index=True)
    last_name = models.CharField(max_length=256, db_index=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, null=True, blank=True)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    first_name = models.CharField(max_length=256, db_index=True)
    last_name = models.CharField(max_length=256, db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    company = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(max_length=256, null=True, blank=True)
    reference = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return f'{self.first_name}' + " " + f'{self.last_name}'


class Log(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    log = models.TextField()