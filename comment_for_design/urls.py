from django.urls import path
from comment_for_designer.views import add_comment, delete_comment

urlpatterns = [

    path('', add_comment),  # [POST]
    path('<int: comment_id>/', delete_comment),  # [DELETE]
]