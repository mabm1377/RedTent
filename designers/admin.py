from django.contrib import admin
from designers.models import Designer, DesignerRecord,CommentForDesigner, RateForDesigner
admin.site.register(Designer)
admin.site.register(DesignerRecord)
admin.site.register(CommentForDesigner)
admin.site.register(RateForDesigner)
# Register your models here.
