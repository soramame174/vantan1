from django.db import models
from django.conf import settings
from django.contrib.auth.models import User  # Userモデルをインポート
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import now

from .consts import MAX_PATE

RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_PATE + 1)]


class MaintenanceConfig(models.Model):
    start_time = models.DateTimeField(verbose_name="開始時間")  # メンテナンス開始時刻
    end_time = models.DateTimeField(verbose_name="終了時間")    # メンテナンス終了時刻
    is_active = models.BooleanField(default=False, verbose_name="オン/オフ")  # メンテナンス有効化スイッチ

class Request(models.Model):
    title = models.CharField(max_length=100, default="タイトルを記入してください", verbose_name="タイトル")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")  # リクエストをしたユーザー
    description = models.TextField(verbose_name="詳細")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")
    text = models.TextField(max_length=450, verbose_name="テキスト")

    def __str__(self):
        return self.title

    # コメント削除用メソッド
    def can_delete_comment(self, user):
        return self.user == user  # リクエストをしたユーザーだけが削除可能

    def get_comments(self):
        return self.comments.all()


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name="コメント")
    request = models.ForeignKey(Request, related_name='comments', on_delete=models.CASCADE, verbose_name="リクエスト")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    content = models.TextField(default="", verbose_name="内容")
    url = models.URLField(blank=True, null=True, verbose_name="URL")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="作成日時")


    def __str__(self):
        return self.content

    # コメント削除用メソッド
    def can_delete(self, user):
        return self.user == user  # コメントをしたユーザーだけが削除可能


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
    ('Healing', '癒し'),
    ('Ragutaimu', 'ラグタイム'),
    ('sound effects', '効果音'),
    ('BGM', 'BGM'),
    ('horror', 'ホラー'),
    ('Japanese style', '和風'),
    ('Western style', '洋風')
)



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# 音楽モデル
class Ongaku(models.Model):
    title = models.CharField(max_length=70, verbose_name="タイトル")
    text = models.TextField(blank=True, default="", verbose_name="説明")
    audio_file = models.FileField(upload_to='music/', null=True, blank=True, verbose_name="音楽ファイル")
    thumbnail = models.ImageField(null=True, blank=True, verbose_name="サムネイル")
    category = models.CharField(
        max_length=200, choices=CATEGORY, null=True, blank=True, verbose_name="カテゴリー"
    )
    custom_category = models.CharField(
        max_length=150,
        blank=True,
        help_text="検索時に見つかりやすくなります。",
        verbose_name="カスタムカテゴリー"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='songs', verbose_name="ユーザー")
    search_count = models.IntegerField(default=0, verbose_name="検索回数")
    play_count = models.IntegerField(default=0, verbose_name="再生回数")

    is_public = models.BooleanField(default=False, verbose_name="公開設定")  # 公開/非公開設定

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")  # 投稿日

    ongaku_url = models.URLField(blank=False, null=False, verbose_name="音楽URL")


    favorites = models.ManyToManyField(User, related_name='favorite_songs', blank=True, verbose_name="お気に入り")

    favorited_by = models.ManyToManyField(
        'UserProfile',  # ユーザー情報が保存されているモデル
        related_name='favorite_songs',
        blank=True,
        verbose_name="お気に入りユーザー"
    )

    order = models.PositiveIntegerField(default=0, verbose_name="順序")

    class Meta:
        ordering = ['order']

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    songs = models.ManyToManyField(Ongaku, verbose_name="作った曲")  # ユーザーが作成した曲の関連
    display_name = models.CharField(max_length=60, unique=True, blank=True, null=True, verbose_name="表示名")
    bio = models.TextField(max_length=35, blank=True, null=True, verbose_name="自己紹介文")  # 自己紹介
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="アイコン")
    youtube_url = models.URLField(blank=True, null=True, verbose_name="YouTube")  # YouTube URL
    twitter_url = models.URLField(blank=True, null=True, verbose_name="x(Twitter)")  # Twitter URL

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
    name = models.CharField(max_length=255, verbose_name="名前")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ユーザー")
    is_public = models.BooleanField(default=False, verbose_name="公開設定")  # 公開・非公開の状態を管理
    songs = models.ManyToManyField(Ongaku, related_name='folders', blank=True, verbose_name="曲")

    def __str__(self):
        return self.name


songs = models.ManyToManyField('Ongaku', blank=True, related_name='folders')



class FolderSong(models.Model):
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, verbose_name="フォルダー")
    song = models.ForeignKey('Ongaku', on_delete=models.CASCADE, verbose_name="曲")

    class Meta:
        unique_together = ('folder', 'song')

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name='following',  # フォローしているユーザー
        on_delete=models.CASCADE,
        verbose_name="フォロー"
    )
    followed = models.ForeignKey(
        User,
        related_name='followers',  # フォロワー
        on_delete=models.CASCADE,
        verbose_name="フォロワー"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # 同じペアの重複を防ぐ

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'

class YourModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
    ongaku = models.ForeignKey(Ongaku, on_delete=models.CASCADE, verbose_name="曲")
    title = models.CharField(max_length=10, verbose_name="タイトル")
    text = models.TextField(verbose_name="テキスト")
    rate = models.IntegerField(choices=RATE_CHOICES, verbose_name="評価")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="投稿ユーザー")

    class Meta:
        unique_together = ('ongaku', 'user')

    def __str__(self):
        return self.title
