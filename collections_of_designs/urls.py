from django.urls import path,re_path
from collections_of_designs.views import user_collection_of_designs, collection_of_design_operations, designs_of_collection

urlpatterns = [

re_path(r'^(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
        user_collection_of_designs),  # [GET, POST]
path('<int:collection_of_design_id>', collection_of_design_operations),  # [GET, PUT, DELETE]
path('<int:collection_of_design_id>/designs/', designs_of_collection)
]