from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Card(models.Model):
    cc_num = models.CharField(max_length=100)
    cvv = models.SmallIntegerField()
    exp_date = models.CharField(max_length=10)
    trans_id = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cc_num