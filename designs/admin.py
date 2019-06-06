from django.contrib import admin
from designs.models import Design, CommentForDesign, RateForDesign
admin.site.register(Design)
admin.site.register(CommentForDesign)
admin.site.register(RateForDesign)
# Register your models here.
