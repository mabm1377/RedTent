from django.urls import path
from comment_for_designer.views import comment_list, delete_comment

urlpatterns = [

    path('', comment_list),  # [POST]
    path('<int: comment_id>/', delete_comment),  # [DELETE]
]