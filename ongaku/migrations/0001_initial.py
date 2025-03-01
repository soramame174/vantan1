# Generated by Django 5.1.6 on 2025-03-01 07:30

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="MaintenanceConfig",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("start_time", models.DateTimeField(verbose_name="開始時間")),
                ("end_time", models.DateTimeField(verbose_name="終了時間")),
                (
                    "is_active",
                    models.BooleanField(default=False, verbose_name="オン/オフ"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ongaku",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=70, verbose_name="タイトル")),
                ("text", models.TextField(blank=True, default="", verbose_name="説明")),
                (
                    "audio_file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="music/",
                        verbose_name="音楽ファイル",
                    ),
                ),
                (
                    "thumbnail",
                    models.ImageField(
                        blank=True, null=True, upload_to="", verbose_name="サムネイル"
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Pop", "ポップ"),
                            ("Rock", "ロック"),
                            ("Jazz", "ジャズ"),
                            ("Classical", "クラシック"),
                            ("Hip-hop", "ヒップホップ"),
                            ("Electronic", "エレクトロニック"),
                            ("Country", "カントリー"),
                            ("Folk", "フォーク"),
                            ("Blues", "ブルース"),
                            ("Reggae", "レゲエ"),
                            ("Metal", "メタル"),
                            ("R&B", "R&B"),
                            ("Punk", "パンク"),
                            ("Techno", "テクノ"),
                            ("Trap", "トラップ"),
                            ("Dubstep", "ダブステップ"),
                            ("Acoustic", "アコースティック"),
                            ("Latin", "ラテン"),
                            ("Soul", "ソウル"),
                            ("Funk", "ファンク"),
                            ("World Music", "ワールドミュージック"),
                            ("Indie", "インディー"),
                            ("House", "ハウス"),
                            ("J-Pop", "J-POP"),
                            ("K-Pop", "K-POP"),
                            ("Synthpop", "シンセポップ"),
                            ("New Wave", "ニューウェーブ"),
                            ("Alternative", "オルタナティヴ"),
                            ("Ambient", "アンビエント"),
                            ("Psychedelic", "サイケデリック"),
                            ("Hardcore", "ハードコア"),
                            ("Rap", "ラップ"),
                            ("City Pop", "シティポップ"),
                            ("Chiptune", "チップチューン"),
                            ("Anison", "アニソン"),
                            ("Future Bass", "フューチャーベース"),
                            ("Vocaloid", "ボカロ"),
                            ("Healing", "癒し"),
                            ("Ragutaimu", "ラグタイム"),
                            ("sound effects", "効果音"),
                            ("BGM", "BGM"),
                            ("horror", "ホラー"),
                            ("Japanese style", "和風"),
                            ("Western style", "洋風"),
                        ],
                        max_length=200,
                        null=True,
                        verbose_name="カテゴリー",
                    ),
                ),
                (
                    "custom_category",
                    models.CharField(
                        blank=True,
                        help_text="検索時に見つかりやすくなります。",
                        max_length=150,
                        verbose_name="カスタムカテゴリー",
                    ),
                ),
                (
                    "search_count",
                    models.IntegerField(default=0, verbose_name="検索回数"),
                ),
                ("play_count", models.IntegerField(default=0, verbose_name="再生回数")),
                (
                    "is_public",
                    models.BooleanField(default=False, verbose_name="公開設定"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                ("ongaku_url", models.URLField(verbose_name="音楽URL")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="順序")),
                (
                    "favorites",
                    models.ManyToManyField(
                        blank=True,
                        related_name="favorite_songs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="お気に入り",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="songs",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Folder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, verbose_name="名前")),
                (
                    "is_public",
                    models.BooleanField(default=False, verbose_name="公開設定"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
                (
                    "songs",
                    models.ManyToManyField(
                        blank=True,
                        related_name="folders",
                        to="ongaku.ongaku",
                        verbose_name="曲",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Request",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="タイトルを記入してください",
                        max_length=100,
                        verbose_name="タイトル",
                    ),
                ),
                ("description", models.TextField(verbose_name="詳細")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="作成日時"
                    ),
                ),
                ("text", models.TextField(max_length=450, verbose_name="テキスト")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=500, verbose_name="コメント")),
                ("content", models.TextField(default="", verbose_name="内容")),
                ("url", models.URLField(blank=True, null=True, verbose_name="URL")),
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="作成日時"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
                (
                    "request",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="ongaku.request",
                        verbose_name="リクエスト",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(
                        blank=True,
                        max_length=60,
                        null=True,
                        unique=True,
                        verbose_name="表示名",
                    ),
                ),
                (
                    "bio",
                    models.TextField(blank=True, null=True, verbose_name="自己紹介文"),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="profile_pictures/",
                        verbose_name="アイコン",
                    ),
                ),
                (
                    "youtube_url",
                    models.URLField(blank=True, null=True, verbose_name="YouTube"),
                ),
                (
                    "twitter_url",
                    models.URLField(blank=True, null=True, verbose_name="x(Twitter)"),
                ),
                (
                    "songs",
                    models.ManyToManyField(to="ongaku.ongaku", verbose_name="作った曲"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="ongaku",
            name="favorited_by",
            field=models.ManyToManyField(
                blank=True,
                related_name="favorite_songs",
                to="ongaku.userprofile",
                verbose_name="お気に入りユーザー",
            ),
        ),
        migrations.CreateModel(
            name="YourModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Follow",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "followed",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="followers",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="フォロワー",
                    ),
                ),
                (
                    "follower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="following",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="フォロー",
                    ),
                ),
            ],
            options={
                "unique_together": {("follower", "followed")},
            },
        ),
        migrations.CreateModel(
            name="FolderSong",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "folder",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ongaku.folder",
                        verbose_name="フォルダー",
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ongaku.ongaku",
                        verbose_name="曲",
                    ),
                ),
            ],
            options={
                "unique_together": {("folder", "song")},
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=10, verbose_name="タイトル")),
                ("text", models.TextField(verbose_name="テキスト")),
                (
                    "rate",
                    models.IntegerField(
                        choices=[
                            (0, "0"),
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                        ],
                        verbose_name="評価",
                    ),
                ),
                (
                    "ongaku",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ongaku.ongaku",
                        verbose_name="曲",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="投稿ユーザー",
                    ),
                ),
            ],
            options={
                "unique_together": {("ongaku", "user")},
            },
        ),
    ]
