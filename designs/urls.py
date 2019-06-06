from django.urls import path
from designs.views import list_of_design, design_operation, list_of_design_tags, list_of_rates_for_design, list_of_comments_for_design, \
    comment_for_design_operations, list_of_a_post_designers, get_myrate
urlpatterns = [

    path(r"", list_of_design),
    path(r'<int:design_id>', design_operation),
    path(r'<int:design_id>/tags/', list_of_design_tags),
    path(r'<int:design_id>/get_my_rate/', get_myrate),  # [GET]
    path(r'<int:design_id>/rates_for_design/', list_of_rates_for_design),
    path(r'<int:design_id>/comments_for_design/', list_of_comments_for_design),
    path(r'<int:design_id>/comments_for_design/<int:comment_id>', comment_for_design_operations),
    path(r'<int:design_id>/designers', list_of_a_post_designers),  # [GET,POST] -token
]