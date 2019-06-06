from django.urls import path, re_path
from tag.views import get_list_designs_of_tags
urlpatterns = [
    path(r'<int:tag_id>/designs/', get_list_designs_of_tags),
]