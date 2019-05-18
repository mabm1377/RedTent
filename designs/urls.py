from django.urls import path, re_path
from designs.views import list_of_design, get_design, test, list_of_design_tags, delete_design_tag, \
    get_myrate,list_of_rates_for_design
urlpatterns = [

    re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$', list_of_design),
    re_path(r'^(_from=(?P<_from>[0-9]*)/)?$', list_of_design),
    re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)&_order_by=(?P<_order_by>[a-zA-z]*)/)?$', list_of_design),
    re_path(r'^(_order_by=(?P<_order_by>[a-zA-z]*)/)?$', list_of_design),

    path('<int:design_id>', get_design),
    re_path(r'^((?P<design_id>[0-9]+))/tags/$', list_of_design_tags),

    path('<int:design_id>/tags/<int:tag_id>', delete_design_tag),#[DELETE]


    path('<int:design_id>/my_rate_for_design/', get_myrate),  # [GET]
    re_path(r'((?P<design_id>[0-9]+))/rate_for_design/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
            list_of_rates_for_design),  # [GET,POST]

    path('<int:design_id>/rate_for_design/<int:rate_for_design_Id>', test),
    # [DELETE, PUT, GET]


    re_path(r'((?P<design_id>[0-9]+))/comments_for_design/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
            test),  # [POST,GET]


    path('<int:design_id>/comments_for_design/<int:comment_Id>', test),
    # [PUT,DELETE,GET],

    path('<int:design_id>/designers', test),  # [GET,POST] -token



]