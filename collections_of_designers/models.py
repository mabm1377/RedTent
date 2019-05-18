from django.db import models
from user_account.models import UserAccount
from designers.models import Designer


class CollectionOfDesigner(models.Model):
    title = models.CharField(max_length=20)
    collectionPicture = models.ImageField(upload_to=None,)
    designer = models.ManyToManyField(Designer)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

# Create your models here.
