from django. urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import increment_play_count

from . import views

# app_name = 'ongaku'  # 名前空間を登録
    

urlpatterns = [

    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('profile/', views.profile_list, name='profile_list'),
    path('ongaku/<int:pk>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('add_song_to_folder/<int:song_id>/', views.add_song_to_folder, name='add_song_to_folder'),
    path('remove_song_from_folder/<int:folder_id>/<int:song_id>/', views.remove_song_from_folder, name='remove_song_from_folder'),
    path('change_display_name/', views.change_display_name, name='change_display_name'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('favorite/<int:song_id>/', views.favorite_song, name='favorite_song'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('register/', views.register, name='register'),
    path('folder/delete/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('profile/', views.profile_list, name='profile'),  # 'profile' という名前を設定
    path('ongaku/<int:ongaku_id>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('toggle-favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),




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