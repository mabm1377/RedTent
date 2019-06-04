from django.urls import path, re_path
from user_account.views import get_token_for_login ,  list_of_users, user_operations, \
    rates_for_tag
urlpatterns = [
    re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$', list_of_users),  # [GET,POST]
    path('<int:user_id>', user_operations),
    path('signin/', get_token_for_login),
    re_path(r'^((?P<user_id>[0-9]+))/rates/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',rates_for_tag),
]