from django.urls import path, re_path
from collections_of_designers.views import user_collection_of_designers,collection_of_designer_operations,designers_of_collection

urlpatterns = [

        re_path(r'', user_collection_of_designers),
        path('<int:collection_of_design_id>', collection_of_designer_operations),  # [GET, PUT, DELETE]
        path('<int:collection_of_design_id>/designers/', designers_of_collection),
]