from django.db import models
from tag.models import Tag
from django.core.validators import RegexValidator


class UserAccount (models.Model):
    firstName = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex='^[a-zA-Z]*$',
        ),
    ])

    lastName = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex='^[a-zA-Z]*$',
        ),
    ])

    username = models.CharField(max_length=20,unique=True, validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
        ),
    ])

    password = models.CharField(max_length=40, validators=[RegexValidator(regex='')])
    isDesigner = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag, through='RateForTag')
    kind = models.CharField(max_length=10, default="user")
    avatar = models.ImageField()


class RateForTag(models.Model):
    rate = models.IntegerField()
    number_of_rating = models.IntegerField(default=0)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='aa')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='bbb')
