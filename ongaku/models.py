from django.db import models
from django.conf import settings
from django.contrib.auth.models import User  # Userモデルをインポート

from .consts import MAX_PATE

RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_PATE + 1)]

# ユーザープロファイルモデル (表示名を追加)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50, verbose_name="表示名", blank=True, null=True)
    class Meta:
        indexes = [
            models.Index(fields=['display_name']),  # display_nameにインデックスを追加
        ]

    def __str__(self):
        return self.display_name if self.display_name else self.user.username
    

COMMON_CATEGORIES = [
    ('ポップ', 'ポップ'),
    ('ロック', 'ロック'),
    ('ジャズ', 'ジャズ'),
    ('クラシック', 'クラシック'),
    ('ヒップホップ', 'ヒップホップ'),
    ('エレクトロニック', 'エレクトロニック'),
    ('カントリー', 'カントリー'),
    ('フォーク', 'フォーク'),
    ('ブルース', 'ブルース'),
    ('レゲエ', 'レゲエ'),
]

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name



# 音楽モデル
class Ongaku(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField(blank=True, default="")
    audio_file = models.FileField(upload_to='music/')
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKeyでCategoryを参照
    custom_category = models.CharField(
        max_length=100,
        blank=True,
        help_text="選択肢にない場合、自由に入力してください。"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    search_count = models.IntegerField(default=0)
    play_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.pk:  
            old_instance = Ongaku.objects.filter(pk=self.pk).first()
            if old_instance and old_instance.audio_file != self.audio_file:
                old_instance.audio_file.delete(save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def get_user_display_name(self):
        # ユーザーの表示名を取得
        if hasattr(self.user, 'profile') and self.user.profile:
            return self.user.profile.display_name if self.user.profile.display_name else self.user.username
        return self.user.username  # UserProfileが存在しない場合は、usernameを表示

    def get_text_display(self):
        return self.text if self.text else "なし"
    
    def get_category_display(self):
        return self.custom_category if self.custom_category else self.category.name if self.category else "なし"
    
    def get_category_display(self):
        if self.custom_category:
            return self.custom_category
        elif self.category:
            return self.category.name
        else:
            return "なし"

class YourModel(models.Model):  # 必要なモデルを定義
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # 修正完了


class Review(models.Model):
    ongaku = models.ForeignKey(Ongaku, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('ongaku', 'user') 

    def __str__(self):
        return self.title
