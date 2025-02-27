# Generated by Django 5.1.6 on 2025-02-27 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ongaku", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ongaku",
            name="category",
            field=models.CharField(
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
                max_length=100,
                null=True,
                verbose_name="カテゴリー",
            ),
        ),
    ]
