from django.urls import path, re_path
from designers.views import test, designer_operation, list_of_all_designers, \
    list_of_comment_designer
urlpatterns = [
re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?', list_of_all_designers),  # [GET,POST]
path('<int:designer_id>', designer_operation),#[GET, PUT, DELETE]
re_path(r'^rates_for_designer/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?', test),
# [GET, POST]
path('designers/rates_for_designer/<int: rates_for_designer_id>', test),  # [DELETE, PUT, GET]
re_path(r'^comments_for_designer?(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?',
        list_of_comment_designer), # [GET, POST]
path('designers/comments_for_designer/<int: rates_for_designer_id>', test)  # [DELETE, PUT, GET]
]
"""
re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$', list_of_design),
re_path(r'^(_from=(?P<_from>[0-9]*)/)?$', list_of_design),
re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)&_order_by=(?P<_order_by>[a-zA-z]*)/)?$', list_of_design),
re_path(r'^(_order_by=(?P<_order_by>[a-zA-z]*)/)?$', list_of_design),
path('<int:design_id>', get_design),
re_path(r'^((?P<design_id>[0-9]+))/tags/$', list_of_design_tags),

path('<int:design_id>/my_rate_for_design/', get_myrate),  # [GET]
re_path(r'^((?P<design_id>[0-9]+))/rate_for_design/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
        list_of_rates_for_design),  # [GET,POST]

path('<int:design_id>/rate_for_design/<int:rate_for_design_id>', rate_for_design_operations),
# [DELETE, PUT, GET]


re_path(r'^((?P<design_id>[0-9]+))/comments_for_design/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
        list_of_comments_for_design),  # [POST,GET]

path('<int:design_id>/comments_for_design/<int:comment_Id>', comment_for_design_operations),
# [DELETE,GET],

path('<int:design_id>/designers', list_of_a_post_designers),  # [GET,POST] -token
"""