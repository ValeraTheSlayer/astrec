"""arec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from card.views import main_page, card_create, card_list, card_detail, card_archive
from users.apps import UsersConfig


urlpatterns = [
    path('', main_page, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace=UsersConfig.name)),
    path('cards/archive/', card_archive, name='card_archive'),
    path('cards/<str:entity>/', card_list, name='card_list'),
    path('card/new/individual/', card_create, name='new_card_individual'),
    path('card/new/legal-entity/', card_create, name='new_card_legal_entity'),
    re_path(r'^card/individuals/(?P<cid>\d+)/$', card_detail, name='card_individual'),
    re_path(r'^card/legal-entiti/(?P<cid>\d+)/$', card_detail, name='card_legal_entity'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
