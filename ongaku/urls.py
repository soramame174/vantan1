from django. urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import increment_play_count

from . import views

# app_name = 'ongaku'  # 名前空間を登録
    

urlpatterns = [
    path('increment-play-count/<int:pk>/', views.increment_play_count, name='increment-play-count'),
    path('restricted/<int:pk>/', views.restricted_view, name='restricted_view'),
    path('', views.index_view, name='index'),
    path('ongaku/', views.ListOngakuView.as_view(), name='list-ongaku'),
    path('ongaku/<int:pk>/datail/', views.DetailOngakuView.as_view(), name='detail-ongaku'),
    path('ongaku/create/', views.CreateOngakuView.as_view(), name='create-ongaku'),
    path('ongaku/<int:pk>/delete/', views.DeleteOngakuView.as_view(), name='delete-ongaku'),
    path('ongaku/<int:pk>/update/', views.UpdateOngakuView.as_view(), name='update-ongaku'),
    path('ongaku/<int:ongaku_id>/review/', views.CreateReviewView.as_view(), name='review'),
    path('search/', views.search_view, name='search'),
    path('delete_history/', views.delete_history, name='delete_history'),  # delete_history のURLパターンが正しいか確認
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)