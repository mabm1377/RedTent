from django.urls import path, re_path
from designers.views import test, designer_operation, list_of_all_designers, \
    list_of_comment_designer, list_of_rate_for_designer,\
    designer_records_operations, list_of_designer_records, get_my_rate
urlpatterns = [
    re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$', list_of_all_designers),  # [GET,POST]

    path('<int:designer_id>', designer_operation),#[GET, PUT, DELETE]

    re_path(r'^rates_for_designer/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
            list_of_rate_for_designer),# [GET, POST]

    path('rates_for_designer/get_my_rate', get_my_rate),

    re_path(r'^comments_for_designer?(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
            list_of_comment_designer),# [GET, POST]
  # [DELETE, PUT, GET]

    re_path(r'^((?P<designer_id>[0-9]+))/designer_records/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
            list_of_designer_records),#[POST,GET]
    re_path(r'^/profile/designer_records/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$', test),
    re_path(r'^/profile/designer_records/((?P<designer_records>[0-9]+))/?$', test),

    path('<int:designer_id>/designer_records/<int:designer_record_id>', designer_records_operations),#[PUT,DELETE,GET]
]
