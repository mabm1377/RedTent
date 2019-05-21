from django.db import models
from tag.models import Tag
from designers.models import Designer
from user_account.models import UserAccount


class Design(models.Model):
    picture = models.ImageField()
    view = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)
    upload_date = models.DateField(auto_now_add=True, blank=True)
    upload_time = models.TimeField(auto_now_add=True, blank=True)
    comments = models.ManyToManyField(UserAccount, through='CommentForDesign' )
    tag = models.ManyToManyField(Tag, related_name='designs')
    designer = models.ManyToManyField(Designer, related_name='designs')
    rate_user = models.ManyToManyField(UserAccount, related_name='designs', through='RateForDesign')


class RateForDesign(models.Model):
    rate = models.IntegerField()
    design = models.ForeignKey(Design,related_name="rates_for_design", on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, related_name="rates_for_design", on_delete=models.CASCADE)


class CommentForDesign(models.Model):
    body = models.CharField(max_length=500)
    isValid = models.BooleanField()
    user = models.ForeignKey(UserAccount, related_name='comments_for_design', on_delete=models.CASCADE)
    design = models.ForeignKey(Design, related_name='comments_for_design', on_delete=models.CASCADE)

