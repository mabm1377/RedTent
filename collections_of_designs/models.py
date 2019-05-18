from django.db import models
from user_account.models import UserAccount
# Create your models here.


class CollectionOfDesign(models.Model):
    title = models.CharField(max_length=20)
    collPic = models.ImageField(upload_to=None,)
    user = models.ForeignKey(UserAccount,related_name='collections_of_design',on_delete=models.CASCADE)
