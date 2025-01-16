from django.contrib import admin
from .models import Ongaku, Review, Category, UserProfile, Request, Comment


from .models import MaintenanceConfig


@admin.register(MaintenanceConfig)
class MaintenanceConfigAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'is_active')


# UserProfileの登録
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name', 'get_user_id')

    def get_user_display_name(self, obj):
        # UserProfileが存在する場合に表示名を取得
        if hasattr(obj.user, 'profile') and obj.user.profile:
            return obj.user.profile.display_name if obj.user.profile.display_name else obj.user.username
        return obj.user.username  # UserProfileが存在しない場合は、usernameを表示

    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.admin_order_field = 'user__id'  # 並べ替え可能にする
    get_user_id.short_description = 'ユーザーID'  # 列名を設定

# Requestモデルを管理画面に登録
@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')  # 表示するカラムを指定
    search_fields = ('title', 'description')  # 検索可能なフィールドを指定
    list_filter = ('created_at', 'user')  # フィルタリングできるフィールドを指定
    actions = ['delete_selected']  # 一括削除を可能にする

    # コメント削除用メソッドを管理画面に追加
    def can_delete_comment(self, obj):
        return obj.user == self.request.user  # リクエストをしたユーザーだけが削除可能

# Commentモデルを管理画面に登録
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'user')  # 表示するカラムを指定
    search_fields = ('content',)  # 検索可能なフィールドを指定
    list_filter = ('user', 'created_at')  # フィルタリングできるフィールドを指定
    actions = ['delete_selected']  # 一括削除を可能にする

# Ongakuモデルの管理画面設定
class OngakuAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'get_user_display_name', 'get_user_id')  # ここに表示名を追加
    list_filter = ('is_public', 'category', 'created_at')
    
    def get_user_display_name(self, obj):
        # UserProfileが存在する場合に表示名を取得
        if hasattr(obj.user, 'profile') and obj.user.profile:
            return obj.user.profile.display_name if obj.user.profile.display_name else obj.user.username
        return obj.user.username  # UserProfileが存在しない場合は、usernameを表示

    get_user_display_name.admin_order_field = 'user__profile__display_name'  # 並べ替え可能にする
    get_user_display_name.short_description = '投稿ユーザー'  # 列名を設定

    def get_user_id(self, obj):
        return obj.user.id
    get_user_id.admin_order_field = 'user__id'  # 並べ替え可能にする
    get_user_id.short_description = 'ユーザーID'  # 列名を設定

# Ongakuを登録する際は、デコレータを使うか、もしくは次のように手動で登録します。
admin.site.register(Ongaku, OngakuAdmin)

# Reviewの登録
admin.site.register(Review)

# Categoryの登録
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)
