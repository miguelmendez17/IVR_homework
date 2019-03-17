from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime

# Create your models here.


class Card(models.Model):
    """
    This model is for representing the request. By default, its called Card because
    it have that the card fields needs
    """
    # cad num
    cc_num = models.CharField(max_length=100)
    # security code
    cvc = models.CharField(max_length=4)
    # month expiration
    exp_month = models.PositiveIntegerField(validators=[MaxValueValidator(12)])
    # year expiration
    exp_year = models.PositiveIntegerField(validators=[MinValueValidator(datetime.now().year), MaxValueValidator(9999)])
    # the amount of the charge
    amount = models.PositiveIntegerField()
    # the description of the charge
    description = models.CharField(max_length=200)
    # This is the date when a transaction is made. By default, it is the current date
    created = models.DateTimeField(default=datetime.now, blank=True)


class CardError(models.Model):
    """
    This model is for log the errors that are generated in transactions.

    """
    # this is the error message
    message = models.CharField(max_length=2000)
    # error status. (200, 400, ..., etc)
    status = models.IntegerField()
    # error code
    code = models.CharField(max_length=100)
    # This is the date when the error happens
    date = models.DateTimeField(default=datetime.now, blank=True)
    # this is the actual name that are logged in the app
    username = models.CharField(max_length=100)


class ResponseTransaction(models.Model):
    """
    This is the model to log all the responses with success
    """
    id = models.CharField(primary_key=True, max_length=100)
    live_mode = models.BooleanField()
    status = models.CharField(max_length=20)
    currency = models.CharField(max_length=10)
    paid = models.BooleanField()
    balance_transaction = models.CharField(max_length=100)
    object_type = models.CharField(max_length=50)
    created = models.IntegerField()
    id_card = models.CharField(max_length=100)
    seller_message = models.CharField(max_length=100)