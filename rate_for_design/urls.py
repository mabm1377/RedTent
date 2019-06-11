from django.conf.urls import url
from rate_for_design.views import post_rate, rate_operation
urlpatterns = [

    url('', post_rate),  # [POST]
    url('<int: rate_for_design>/', rate_operation),  # [GET, PUT]
]