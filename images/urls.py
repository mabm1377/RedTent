from django.urls import path, re_path
from images.views import image
urlpatterns = [
    path('<str:path>', image),
]