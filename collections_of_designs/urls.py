from django.urls import path,re_path
from collections_of_designs.views import user_collection_of_designs, test

urlpatterns = [

re_path(r'collections_of_designs/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?',
        user_collection_of_designs),  # [GET, POST]
path('collections_of_designs/<int:collection_of_design_id>', test),  # [GET, PUT, DELETE]
]