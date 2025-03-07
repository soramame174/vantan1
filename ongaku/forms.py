from django import forms
from .models import Ongaku, Category, UserProfile, Folder, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['display_name', 'bio', 'profile_picture', 'youtube_url', 'twitter_url']  # 必要なフィールドを追加

    def clean_display_name(self):
        display_name = self.cleaned_data.get('display_name')
        if display_name and display_name.strip():
            if UserProfile.objects.exclude(id=self.instance.id).filter(display_name=display_name).exists():
                raise forms.ValidationError("この表示名はすでに使用されています。別の名前を選んでください。")
        return display_name


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'url']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'コメントを入力...'}),
        }
        text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'コメントを入力してください...'}))

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']  # フォルダ名を入力可能
        labels = {
            'name': 'フォルダ名',
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User  # Userを使うことができます
        fields = ['username', 'email', 'password1', 'password2']

class AddSongToFolderForm(forms.Form):
    folder = forms.ModelChoiceField(queryset=Folder.objects.none(), required=True, label="フォルダを選択")
    song = forms.ModelChoiceField(queryset=Ongaku.objects.none(), required=True, label="音楽")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 現在ログインしているユーザーを取得
        song = kwargs.pop('song', None)  # 音楽の初期値を受け取る
        super().__init__(*args, **kwargs)
        if user:
            # ユーザー固有のフォルダだけを表示
            self.fields['folder'].queryset = Folder.objects.filter(user=user)
        if song:
            # 曲の初期値を設定
            self.fields['song'].initial = song
            self.fields['song'].queryset = Ongaku.objects.all()  # 曲は全ユーザーのものを表示

# OngakuFormクラスの修正
class OngakuForm(forms.ModelForm):
    class Meta:
        model = Ongaku
        fields = ['title', 'text', 'audio_file', 'thumbnail', 'category', 'custom_category', 'ongaku_url', 'is_public']
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label="カテゴリ")
    ongaku_url = forms.URLField(required=True, label="URL")
    widgets = {
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),  # チェックボックスをレンダリング
        }
    
    def __str__(self):
        return self.title
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        # 編集の場合は現在のタイトルを除外して重複をチェック
        if self.instance.pk:
            existing_title = Ongaku.objects.exclude(pk=self.instance.pk).filter(title=title)
        else:
            existing_title = Ongaku.objects.filter(title=title)

        if existing_title.exists():
            raise forms.ValidationError("このタイトルはすでに存在しています。別のタイトルを選んでください。")
        return title
    
    def clean_ongaku_url(self):
        ongaku_url = self.cleaned_data.get('ongaku_url')
        if not ongaku_url or not ongaku_url.strip():
            raise forms.ValidationError("URLを入力してください。")
        return ongaku_url





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
