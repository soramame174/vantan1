from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('requests/', views.request_view, name='request_view'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),
    path('requests/delete/<int:request_id>/', views.delete_request, name='delete_request'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    # ユーザープロフィール関連
    path('follow/<int:user_id>/', views.follow_user, name='follow'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow'),
    path('profile/<int:user_id>/', views.user_profile, name='profile'),
    path('profile/', views.profile_list, name='profile_list'),

    # お気に入りとフォルダ管理
    path('toggle_favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('ongaku/<int:pk>/favorite/', views.toggle_favorite, name='toggle-favorite'),
    path('add_song_to_folder/<int:song_id>/', views.add_song_to_folder, name='add_song_to_folder'),
    path('remove_song_from_folder/<int:folder_id>/<int:song_id>/', views.remove_song_from_folder, name='remove_song_from_folder'),
    path('create_folder/', views.create_folder, name='create_folder'),
    path('folder/<int:folder_id>/', views.folder_detail, name='folder_detail'),
    path('toggle_folder_visibility/<int:folder_id>/', views.toggle_folder_visibility, name='toggle_folder_visibility'),
    path('folder/<int:folder_id>/update/', views.update_folder_name, name='update_folder_name'),
    path('folder/<int:folder_id>/update_order/', views.update_song_order, name='update_song_order'),
    path('folder/delete/<int:folder_id>/', views.delete_folder, name='delete_folder'),
    path('public_folders/', views.public_folders, name='public_folders'),

    # その他の機能
    path('register/', views.register, name='register'),
    path('increment-play-count/<int:pk>/', views.increment_play_count, name='increment-play-count'),
    path('restricted/<int:pk>/', views.restricted_view, name='restricted_view'),
    path('change_display_name/', views.change_display_name, name='change_display_name'),
    path('delete_history/', views.delete_history, name='delete_history'),

    # トップページとインデックス
    path('top/', views.top, name='top'),  # トップページ
    path('top/about/', views.about, name='about'),

    path('', views.index_view, name='index'),  # ルートURLにindex_viewを割り当て

    # 音楽関連のCRUDとリスト表示
    path('ongaku/', views.ListOngakuView.as_view(), name='list-ongaku'),
    path('ongaku/<int:pk>/datail/', views.DetailOngakuView.as_view(), name='detail-ongaku'),
    path('ongaku/create/', views.CreateOngakuView.as_view(), name='create-ongaku'),
    path('ongaku/<int:pk>/delete/', views.DeleteOngakuView.as_view(), name='delete-ongaku'),
    path('ongaku/<int:pk>/update/', views.UpdateOngakuView.as_view(), name='update-ongaku'),
    path('ongaku/<int:ongaku_id>/review/', views.CreateReviewView.as_view(), name='review'),

    # 検索
    path('search/', views.search_view, name='search'),
]

# 静的ファイルとメディアファイルの設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
