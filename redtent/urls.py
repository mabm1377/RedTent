"""redtent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'designs/', include('designs.urls')),
    path(r'designers/', include('designers.urls')),
    path(r'users/', include('user_account.urls')),
    path(r'collection_of_designs/', include('collections_of_designs.urls')),
    path(r'collections_of_designers/', include('collections_of_designers.urls')),
    path(r'rate_for_designer/', include('rate_for_designer.urls')),
    path(r'comment_for_designer/', include('comment_for_designer.urls')),
    path(r'rate_for_tags/', include('user_account.urls')),
    path(r'site_images/', include('site_images.urls')),
    url(r'^docs/', include_docs_urls(title='My API title')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
