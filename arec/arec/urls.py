from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from card.views import main_page, card_create, card_list, card_detail, card_archive, card_statistics, \
                    card_approval_registry, merge_pdfs, download_selected_cards
from users.apps import UsersConfig


urlpatterns = [
    path('', main_page, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls', namespace=UsersConfig.name)),
    path('cards/archive/', card_archive, name='card_archive'),
    path('cards/registry/', card_approval_registry, name='card_registry'),
    re_path(r'^cards/(?P<entity>individual|legal)/$', card_list, name='card_list'),
    path('card_statistics/', card_statistics, name='card_statistics'),
    path('card/new/individual/', card_create, name='new_card_individual'),
    path('card/new/legal-entity/', card_create, name='new_card_legal_entity'),
    path('card/<int:cid>/', card_detail, name='card_detail'),
    path('card/<int:cid>/merge_pdfs/', merge_pdfs, name='merge_pdfs'),
    path('download_selected/', download_selected_cards, name='download_selected'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # TODO: do it properly with nginx
