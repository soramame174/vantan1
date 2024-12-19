from django.contrib import admin

from .models import Ongaku, Review, Category, UserProfile

# UserProfileの登録
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name')

# Ongakuモデルの管理画面設定
class OngakuAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'custom_category')
    list_filter = ('category',)

# Ongakuを登録する際は、デコレータを使うか、もしくは次のように手動で登録します。
admin.site.register(Ongaku, OngakuAdmin)

# Reviewの登録
admin.site.register(Review)

# Categoryの登録
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Category, CategoryAdmin)
