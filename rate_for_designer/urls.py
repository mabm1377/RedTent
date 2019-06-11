from django.conf.urls import url
from rate_for_designer.views import post_rate, rate_operation
urlpatterns = [

    url('', post_rate),  # [POST]
    url('<int: rate_for_designer_id>/', rate_operation),  # [GET, PUT]
]