from django.urls import path, re_path
from user_account.views import get_token_for_login ,  list_of_users, user_operations, \
    rates_for_tag
urlpatterns = [
    path(r'', list_of_users),  # [GET,POST]
    path(r'<int:user_id>', user_operations),
    path(r'signin/', get_token_for_login),
    path(r'<int:user_id>/rates/', rates_for_tag),
]