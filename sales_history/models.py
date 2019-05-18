from django.db import models
from user_account.models import UserAccount
from designers.models import Designer
from designs.models import Design


class SalesHistory(models.Model):
    user = models.ForeignKey(UserAccount, related_name="sales_history", on_delete=models.CASCADE)
    designer =models.ForeignKey(Designer, related_name="sales_history", on_delete=models.CASCADE)
    design = models.ForeignKey(Design, related_name="sales_history", on_delete=models.CASCADE)

# Create your models here.
