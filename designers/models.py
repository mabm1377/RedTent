from django.db import models
from django.core.validators import RegexValidator
from user_account.models import UserAccount


class Designer(models.Model):
    user = models.OneToOneField(UserAccount, related_name='designer', on_delete=models.CASCADE)
    phoneNumber = models.IntegerField(validators=[RegexValidator(regex='')])
    city = models.CharField(max_length=20, validators=[RegexValidator(regex='')])
    address = models.CharField(max_length=150)
    comments = models.ManyToManyField(UserAccount, through='CommentForDesigner',related_name='Designer1')
    rates = models.ManyToManyField(UserAccount, through='RateForDesigner',related_name='Designer2')


class RateForDesigner(models.Model):
    rate = models.IntegerField()
    user = models.ForeignKey(UserAccount, related_name='rates_for_designer', on_delete=models.CASCADE)
    designer = models.ForeignKey(Designer, related_name='rates_for_designer', on_delete=models.CASCADE)


class DesignerRecord(models.Model):
    pic = models.ImageField()
    description = models.CharField(max_length=500)
    designer = models.ForeignKey(Designer, related_name='designer_records', on_delete=models.CASCADE)


class CommentForDesigner(models.Model):
    body = models.CharField(max_length=500)
    isvalid = models.BooleanField()
    user = models.ForeignKey(UserAccount, related_name='comments_for_designer', on_delete=models.CASCADE)
    designer = models.ForeignKey(Designer, related_name='comments_for_designer', on_delete=models.CASCADE)


# Create your models here.
