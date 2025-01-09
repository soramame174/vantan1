from django.db import models
from django.conf import settings
from django.contrib.auth.models import User  # Userモデルをインポート
from django.core.exceptions import ValidationError
from django.utils.timezone import now

from .consts import MAX_PATE

RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_PATE + 1)]


class MaintenanceConfig(models.Model):
    start_time = models.DateTimeField()  # メンテナンス開始時刻
    end_time = models.DateTimeField()    # メンテナンス終了時刻
    is_active = models.BooleanField(default=False)  # メンテナンス有効化スイッチ

CATEGORY = (
    ('Pop', 'ポップ'),
    ('Rock', 'ロック'),
    ('Jazz', 'ジャズ'),
    ('Classical', 'クラシック'),
    ('Hip-hop', 'ヒップホップ'),
    ('Electronic', 'エレクトロニック'),
    ('Country', 'カントリー'),
    ('Folk', 'フォーク'),
    ('Blues', 'ブルース'),
    ('Reggae', 'レゲエ'),
    ('Metal', 'メタル'),
    ('R&B', 'R&B'),
    ('Punk', 'パンク'),
    ('Techno', 'テクノ'),
    ('Trap', 'トラップ'),
    ('Dubstep', 'ダブステップ'),
    ('Acoustic', 'アコースティック'),
    ('Latin', 'ラテン'),
    ('Soul', 'ソウル'),
    ('Funk', 'ファンク'),
    ('World Music', 'ワールドミュージック'),
    ('Indie', 'インディー'),
    ('House', 'ハウス'),
    ('J-Pop', 'J-POP'),
    ('K-Pop', 'K-POP'),
    ('Synthpop', 'シンセポップ'),
    ('New Wave', 'ニューウェーブ'),
    ('Alternative', 'オルタナティヴ'),
    ('Ambient', 'アンビエント'),
    ('Psychedelic', 'サイケデリック'),
    ('Hardcore', 'ハードコア'),
    ('Rap', 'ラップ'),
    ('City Pop', 'シティポップ'),
    ('Chiptune', 'チップチューン'),
    ('Anison', 'アニソン'),
    ('Future Bass', 'フューチャーベース'),
    ('Vocaloid', 'ボカロ'),
    ('Healing', '癒し')
)



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 音楽モデル
class Ongaku(models.Model):
    title = models.CharField(max_length=70)
    text = models.TextField(blank=True, default="")
    audio_file = models.FileField(upload_to='music/', null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True)
    category = models.CharField(
        max_length=100, choices=CATEGORY, null=True, blank=True
    ) 
    custom_category = models.CharField(
        max_length=100,
        blank=True,
        help_text="検索時に見つかりやすくなります。"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs')
    search_count = models.IntegerField(default=0)
    play_count = models.IntegerField(default=0)

    is_public = models.BooleanField(default=False)  # 公開/非公開設定

    created_at = models.DateTimeField(auto_now_add=True)  # 投稿日

    ongaku_url = models.URLField(blank=False, null=False)

    favorites = models.ManyToManyField(User, related_name='favorite_songs', blank=True)

    favorited_by = models.ManyToManyField(
        'UserProfile',  # ユーザー情報が保存されているモデル
        related_name='favorite_songs',
        blank=True
    )

    @property
    def has_audio_file(self):
        return bool(self.audio_file)  # audio_file が存在すれば True を返す

    def save(self, *args, **kwargs):

        # タイトルの重複をチェック
        if Ongaku.objects.filter(title=self.title).exclude(pk=self.pk).exists():
            raise ValidationError(f"タイトル「{self.title}」はすでに存在します。別のタイトルを入力してください。")

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
        if self.custom_category:
            return self.custom_category
        elif self.category:
            return self.category.name
        else:
            return "なし"


# ユーザープロファイルモデル (表示名を追加)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Ongaku)  # ユーザーが作成した曲の関連
    display_name = models.CharField(max_length=100, unique=True, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # 自己紹介
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)  # YouTube URL
    twitter_url = models.URLField(blank=True, null=True)  # Twitter URL

    def clean(self):
        # display_nameが空でない場合のみ重複チェックを行う
        if self.display_name and self.display_name.strip():  # 空白以外の文字が含まれている場合
            # 他のユーザーと重複しているかをチェック
            if UserProfile.objects.exclude(id=self.id).filter(display_name=self.display_name).exists():
                raise ValidationError({'display_name': 'この表示名はすでに使用されています。別の名前を選んでください。'})


    def save(self, *args, **kwargs):
        # モデルのクリーンメソッドを呼び出してバリデーションを実行
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Folder(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Ongaku, related_name='folders', blank=True)

    def __str__(self):
        return self.name


songs = models.ManyToManyField('Ongaku', blank=True, related_name='folders')



class FolderSong(models.Model):
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
    song = models.ForeignKey('Ongaku', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('folder', 'song')  # 必要に応じてユニーク制約を設定

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='following',  # フォローしているユーザー
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User,
        related_name='followers',  # フォロワー
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # 同じペアの重複を防ぐ

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'
    
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
