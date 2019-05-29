from django.urls import path, re_path
from designers.views import test, designer_operation, list_of_all_designers, \
    list_of_comment_designer, list_of_rate_for_designer, rate_for_designers_operations,\
    designer_records_operations, list_of_designer_records
urlpatterns = [
    re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?', list_of_all_designers),  # [GET,POST]

    path('<int:designer_id>', designer_operation),#[GET, PUT, DELETE]

    re_path(r'^rates_for_designer/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?',
            list_of_rate_for_designer),# [GET, POST]

    path('rates_for_designer/<int: rates_for_designer_id>', rate_for_designers_operations),  # [DELETE, PUT, GET]

    re_path(r'^comments_for_designer?(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?',
            list_of_comment_designer), # [GET, POST]

    path('comments_for_designer/<int: rates_for_designer_id>', test),  # [DELETE, PUT, GET]

    re_path(r'^((?P<designer_id>[0-9]+))/designer_records/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
            list_of_rate_for_designer),#[POST,GET]

    path('<int:designer_id>/designer_records/<int:designer_record_id>', designer_records_operations),#[PUT,DELETE,GET]
]
