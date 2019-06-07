from django.db import models
from user_account.models import UserAccount
from designs.models import Design
# Create your models here.


class CollectionOfDesign(models.Model):
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to=None,)
    user = models.ForeignKey(UserAccount, related_name='collections_of_design', on_delete=models.CASCADE, blank=True)
    designs = models.ManyToManyField(Design, related_name='collections_of_design')
