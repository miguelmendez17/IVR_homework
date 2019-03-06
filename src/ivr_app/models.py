from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime

actual_date = datetime.datetime.now()

# Create your models here.


class Card(models.Model):
    cc_num = models.CharField(max_length=100)
    cvc = models.CharField(max_length=4)
    exp_month = models.PositiveIntegerField(validators=[MaxValueValidator(12)])
    exp_year = models.PositiveIntegerField(validators=[MinValueValidator(actual_date.year), MaxValueValidator(9999)])
    trans_id = models.CharField(max_length=100)

    def __str__(self):
        return self.cc_num


class CardError(models.Model):
    message = models.CharField(max_length=500)
    status = models.IntegerField()
    code = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True)