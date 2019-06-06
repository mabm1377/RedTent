from django.urls import path, re_path
from designers.views import  designer_operation, list_of_all_designers, \
    list_of_comment_designer, list_of_rate_for_designer,\
    designer_records_operations, list_of_designer_records, get_my_rate
urlpatterns = [
    path(r'', list_of_all_designers),
    path(r'<int:designer_id>', designer_operation),
    path(r'<int:designer_id>/get_my_rate/', get_my_rate),
    path(r'rates_for_designer/', list_of_rate_for_designer),
    path('rates_for_designer/get_my_rate', get_my_rate),
    path(r'comments_for_designer/', list_of_comment_designer),
    path(r'designer_records/',list_of_designer_records),#[POST,GET]
    path('<int:designer_id>/designer_records/<int:designer_record_id>', designer_records_operations),#[PUT,DELETE,GET]
]
