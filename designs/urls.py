from django.urls import path, re_path
from designs.views import list_of_design, get_design, list_of_design_tags, list_of_rates_for_design, \
    rate_for_design_operations, list_of_comments_for_design, comment_for_design_operations, list_of_a_post_designers,\
    get_myrate
urlpatterns = [

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
    # [PUT,DELETE,GET],

    path('<int:design_id>/designers', list_of_a_post_designers),  # [GET,POST] -token

]