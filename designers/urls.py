from django.urls import path, re_path
from designers.views import test, designer_operation, list_of_all_designers
urlpatterns = [
re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?', list_of_all_designers),  # [GET,POST]
path('<int:designer_id>', designer_operation),#[GET, PUT, DELETE]
re_path(r'^rates_for_designer/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?', test),
# [GET, POST]
path('designers/rates_for_designer/<int: rates_for_designer_id>', test),  # [DELETE, PUT, GET]
re_path(r'^comments_for_designer?(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?', test),
# [GET, POST]
path('designers/comments_for_designer/<int: rates_for_designer_id>', test)  # [DELETE, PUT, GET]
]