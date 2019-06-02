from django.urls import path, re_path
from tag.views import get_list_designs_of_tags
urlpatterns = [
    re_path(r'^((?P<tag_id>[0-9]+))/designs/(_from=(?P<_from>[0-9]*)&_row=(?P<_row>[0-9]*)/)?$',
            get_list_designs_of_tags),
]