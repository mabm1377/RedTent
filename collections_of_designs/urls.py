from django.urls import path
from collections_of_designs.views import user_collection_of_designs, collection_of_design_operations,\
        designs_of_collection

urlpatterns = [

path(r'', user_collection_of_designs),
path('<int:collection_of_design_id>', collection_of_design_operations),
path('<int:collection_of_design_id>/designs/', designs_of_collection),
]