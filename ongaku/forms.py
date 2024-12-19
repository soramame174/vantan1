from django import forms
from .models import Ongaku, Category

from django.core.management.base import BaseCommand

# OngakuFormクラスの修正
class OngakuForm(forms.ModelForm):
    class Meta:
        model = Ongaku
        fields = ['title', 'text', 'audio_file', 'thumbnail', 'category', 'custom_category']
        # 'search_count' はモデル側で定義するので、フォームには含めません
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="カテゴリ")

    def __str__(self):
        return self.title

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        custom_category = cleaned_data.get('custom_category')

        # カテゴリーも新しいカテゴリーも未入力の場合エラー
        if not category and not custom_category:
            raise forms.ValidationError("カテゴリーを選択するか、自由に入力してください。")
        return cleaned_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = [
            'ポップ', 'ロック', 'ジャズ', 'クラシック', 'ヒップホップ',
            'エレクトロニック', 'カントリー', 'フォーク', 'ブルース', 'レゲエ'
        ]
        for name in categories:
            Category.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('初期カテゴリーが登録されました。'))

# 検索フォーム（SearchForm）はそのままで問題なし
class SearchForm(forms.Form):
    query = forms.CharField(label='検索', max_length=100, required=False)


