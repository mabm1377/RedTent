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

    username = models.CharField(max_length=20, validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9]*$',
        ),
    ])

    password = models.CharField(max_length=40, validators=[RegexValidator(regex='')])
    isDesigner = models.BooleanField(default=False)
    tag = models.ManyToManyField(Tag,through='RateForTag')
    token = models.CharField(max_length=100, unique=True)
    kind = models.CharField(max_length=10)


class RateForTag(models.Model):
    rate = models.IntegerField()
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='aa')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,related_name='bbb')
