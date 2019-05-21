from django.urls import path, re_path
from user_account.views import get_token_for_login , get_token_for_signup, get_list_of_users, user_operations
urlpatterns = [
    re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?', get_list_of_users),  # [GET,POST]
    path('<int:user_id>', user_operations),#[GET, PUT, DELETE]
    path('signin/', get_token_for_login),
    path('signup/', get_token_for_signup)
]