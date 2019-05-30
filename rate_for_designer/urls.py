from django.urls import path
from rate_for_designer.views import post_rate, rate_operation
urlpatterns = [

    path('', post_rate),  # [POST]
    path('<int: rate_for_designer_id>/', rate_operation),  # [GET, PUT]
]