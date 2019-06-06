from django.urls import path
from site_images.views import add_image
urlpatterns = [
    path(r"", add_image)
]
