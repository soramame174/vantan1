from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from .models import YourModel
from django.db.models import Avg, Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .forms import OngakuForm, FolderForm, UserProfileForm, Folder, AddSongToFolderForm, RegisterForm
from .models import Ongaku, Review, UserProfile, User, Follow
from .models import Folder
from .consts import ITEM_PER_PAGE
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
    )
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from django.contrib import messages

import logging
# from django.utils import timezone
# import pytz  # pytzをインポート

from .models import MaintenanceConfig
from django.http import HttpResponse
import datetime


from .forms import DarkModeScheduleForm
from .models import DarkModeSchedule
from django.utils.timezone import now



def check_maintenance():
    config = MaintenanceConfig.objects.filter(is_active=True).first()
    if config:
        now = datetime.datetime.now()
        if config.start_time <= now <= config.end_time:
            return True
    return False

def my_view(request):
    if check_maintenance():
        return HttpResponse("現在メンテナンス中です。後ほどお試しください。", status=503)
    return HttpResponse("アプリケーションは動作中です。")




# ダークモードのスケジュールを設定するビュー
def set_dark_mode_schedule(request):
    try:
        schedule = DarkModeSchedule.objects.get(user=request.user)
    except DarkModeSchedule.DoesNotExist:
        schedule = None

    if request.method == 'POST':
        form = DarkModeScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            dark_schedule = form.save(commit=False)
            dark_schedule.user = request.user
            dark_schedule.save()
            return redirect('success_page')  # 設定完了後のページにリダイレクト
    else:
        form = DarkModeScheduleForm(instance=schedule)

    context = {
        'user': request.user,  # 正しいユーザーを渡す
        'dark_mode_schedule': schedule,  # ユーザーのダークモードスケジュールを渡す
        'is_active': schedule.is_active if schedule else False,  # ダークモードが有効かを渡す
    }

    return render(request, 'set_dark_mode.html', context)




# 設定成功ページのビュー
def success_page(request):
    return render(request, 'success_page.html')




logger = logging.getLogger(__name__)

@login_required
def follow_user(request, user_id):
    followed_user = get_object_or_404(User, pk=user_id)
    
    # フォロー済みか確認
    is_following = Follow.objects.filter(follower=request.user, followed=followed_user).exists()

    if is_following:
        # フォロー解除
        Follow.objects.filter(follower=request.user, followed=followed_user).delete()
    else:
        # フォロー追加
        Follow.objects.create(follower=request.user, followed=followed_user)

    # フォロワー数を更新
    follower_count = followed_user.followers.count()
    following_count = request.user.following.count()

    # プロフィールページにリダイレクト
    return redirect('profile', user_id=user_id)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow)

    if follow.exists():
        follow.delete()

    # フォロワー数を更新
    follower_count = user_to_unfollow.followers.count()
    following_count = request.user.following.count()

    # プロフィールページにリダイレクト
    return redirect('profile', user_id=user_to_unfollow.id)


def user_profile(request, user_id):
    """ユーザーのプロフィールページを表示"""
    user = get_object_or_404(User, pk=user_id)  # ユーザーを取得
    profile = user.userprofile  # ユーザーのプロフィール情報を取得

    # ログインしているユーザーがそのユーザーをフォローしているかどうかを確認
    is_following = Follow.objects.filter(follower=request.user, followed=profile.user).exists() if request.user.is_authenticated else False

    # ユーザーが作成した曲を取得
    songs = user.songs.all()

    # 音楽ファイルがあるかどうかを確認
    has_audio_file = any(song.audio_file for song in songs)  # もし音楽ファイルがある曲があればTrue

    # フォロー中のユーザーを取得
    followed_users = User.objects.filter(
        id__in=Follow.objects.filter(follower=request.user).values('followed')
    )  # フォロー中のユーザーを取得

    # 自分のプロフィールかどうかを判定
    is_own_profile = request.user == user  # 自分のプロフィールページの場合 True

    # フォロワー数とフォロー数を取得
    follower_count = Follow.objects.filter(followed=user).count()  # フォロワー数を取得
    following_count = Follow.objects.filter(follower=user).count()  # フォローしているユーザー数を取得

    return render(request, 'ongaku/profile.html', {
        'profile': profile,
        'user': user,
        'is_following': is_following,
        'songs': songs,
        'followed_users': followed_users,  # フォロー中のユーザーを渡す
        'is_own_profile': is_own_profile,  # 自分のプロフィールかどうかを渡す
        'follower_count': follower_count,
        'following_count': following_count,
        'has_audio_file': has_audio_file,  # 音楽ファイルがあるかどうかのフラグを渡す
    })


def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        user = request.user
        folders = user.userprofile.folders.all() if hasattr(user, 'userprofile') else []
        
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    # フォロワー数とフォロー数を取得
    follower_count = Follow.objects.filter(following=request.user).count()
    following_count = Follow.objects.filter(follower=request.user).count()

    # デバッグ用のログ出力
    logger.debug(f"follower_count: {follower_count}, following_count: {following_count}")

    return render(request, 'ongaku/profile.html', {
        'form': form,
        'user': request.user,
        'folders': folders,
        'follower_count': follower_count,
        'following_count': following_count,
    })



@login_required
def folder_list(request):
    """ユーザー固有のフォルダを表示する"""
    folders = Folder.objects.filter(user=request.user)  # ログイン中のユーザーに関連するフォルダを取得
    return render(request, 'ongaku/folder_list.html', {'folders': folders})


@login_required
def add_song_to_folder(request, song_id):
    """フォルダに音楽を追加する"""
    song = get_object_or_404(Ongaku, id=song_id)
    user_folders = Folder.objects.filter(user=request.user)

    # すでに曲が追加されているフォルダを除外
    existing_folders = song.folders.all()  # 既に曲が追加されているフォルダを取得
    available_folders = user_folders.exclude(id__in=existing_folders.values('id'))

    if request.method == "POST":
        form = AddSongToFolderForm(request.POST, user=request.user, song=song)
        if form.is_valid():
            folder = form.cleaned_data['folder']
            # 曲がまだそのフォルダに追加されていない場合、追加する
            if song not in folder.songs.all():
                folder.songs.add(song)
                messages.success(request, f"{song.title} を {folder.name} に追加しました！")
            else:
                messages.info(request, f"{song.title} はすでに {folder.name} に存在します。")
            return redirect('profile_list')
    else:
        # 初期データ付きフォームを作成
        form = AddSongToFolderForm(initial={'folder': None}, user=request.user, song=song)

    return render(request, 'ongaku/add_song_to_folder.html', {
        'form': form,
        'song': song,
        'user_folders': available_folders  # 追加されていないフォルダだけを渡す
    })



def add_to_favorites(request, pk):
    song = get_object_or_404(Ongaku, pk=pk)
    user_profile = request.user.userprofile
    if song not in user_profile.favorite_songs.all():
        user_profile.favorite_songs.add(song)
    else:
        user_profile.favorite_songs.remove(song)
    return redirect('profile')  # または適切なURLにリダイレクト

def remove_song_from_folder(request, folder_id, song_id):
    """フォルダから音楽を削除する"""
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)  # ユーザー所有のフォルダ
    song = get_object_or_404(Ongaku, id=song_id)

    if request.method == "POST":
        if song in folder.songs.all():
            folder.songs.remove(song)
            messages.success(request, f"{song.title} をフォルダから削除しました。")
        else:
            messages.error(request, "このフォルダに指定された音楽は存在しません。")
    return redirect('folder_detail', folder_id=folder.id)  # 適切なリダイレクト先を指定

@login_required
def toggle_favorite(request, pk):
    ongaku = get_object_or_404(Ongaku, pk=pk)
    if ongaku in request.user.favorite_songs.all():
        request.user.favorite_songs.remove(ongaku)
        favorited = False
    else:
        request.user.favorite_songs.add(ongaku)
        favorited = True

    # お気に入り登録者数
    favorite_count = ongaku.favorites.count()

    return JsonResponse({
        'favorited': favorited,
        'count': favorite_count,
    })



@login_required
def profile(request, user_id):
    """ユーザープロフィール表示"""
    user_profile = request.user.userprofile
    favorite_songs = user_profile.favorite_songs.all()  # UserProfileに保存されているお気に入りの曲を取得
    folders = Folder.objects.filter(user=user_profile.user)  # フォルダを取得

    # ログインしているユーザーがフォローしているユーザーを取得
    if request.user.is_authenticated:
        followed_users = User.objects.filter(
            id__in=Follow.objects.filter(follower=request.user).values('followed')
        )
    else:
        followed_users = User.objects.none()  # 未ログイン時は空のクエリセット
    

    context = {
        'user': user_profile.user,
        'folders': folders,
        'favorite_songs': favorite_songs,
        'followed_users': followed_users,  # フォロー中のユーザーを渡す
    }

    return render(request, 'ongaku/profile_list.html', context)

@login_required
def change_display_name(request):
    """プロフィール設定ページ"""
    user_profile = UserProfile.objects.get(user=request.user)

    # フォームの送信処理
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            # 表示名が変更された場合のみ重複チェックを行う
            display_name = form.cleaned_data['display_name']
            if display_name != user_profile.display_name:  # 変更された場合のみチェック
                if UserProfile.objects.filter(display_name=display_name).exclude(user=request.user).exists():
                    form.add_error('display_name', 'この名前はすでに他のユーザーによって使用されています。別の名前を選んでください。')
                else:
                    form.save()  # 名前が重複していなければ保存
                    messages.success(request, "表示名が変更されました！")
                    return redirect('profile', user_id=request.user.id)  # 編集後はプロフィールページにリダイレクト
            else:
                # 表示名が変更されていない場合はそのまま保存
                form.save()
                messages.success(request, "表示名が変更されました！")
                return redirect('profile', user_id=request.user.id)
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'ongaku/change_display_name.html', {'form': form})



@login_required
def create_folder(request):
    """フォルダ作成"""
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            messages.success(request, "フォルダが作成されました！")
            return redirect('profile_list')
    else:
        form = FolderForm()
    return render(request, 'ongaku/create_folder.html', {'form': form})

# フォルダ詳細ページ
def folder_detail(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    return render(request, 'ongaku/folder_detail.html', {'folder': folder})

# フォルダ削除
def delete_folder(request, folder_id):
    folder = Folder.objects.get(id=folder_id)
    folder.delete()
    return redirect(reverse('profile'))


@login_required
def favorite_song(request, song_id):
    """お気に入り曲登録"""
    song = get_object_or_404(Ongaku, id=song_id)
    user_profile = request.user.userprofile
    user_profile.favorite_songs.add(song)
    messages.success(request, f"{song.title}がお気に入りに追加されました！")
    return redirect('profile_list')


@login_required
def profile_list(request):
    """プロフィールリスト表示"""
    # UserProfileが存在しない場合は作成
    try:
        userprofile = request.user.userprofile
    except UserProfile.DoesNotExist:
        userprofile = UserProfile.objects.create(user=request.user)
        messages.info(request, "プロフィールが自動的に作成されました。")

    folders = Folder.objects.filter(user=request.user)  # ユーザーのフォルダを取得
    return render(request, 'ongaku/profile_list.html', {'userprofile': userprofile, 'folders': folders})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        display_name = request.POST.get('display_name')  # フォームから表示名を取得
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'ongaku/register.html', {'error': 'パスワードが一致しません。'})

        if User.objects.filter(username=username).exists():
            return render(request, 'ongaku/register.html', {'error': 'そのユーザー名は既に使用されています。'})

        user = User.objects.create_user(username=username, password=password1)
        UserProfile.objects.create(user=user, display_name=display_name)  # UserProfileに表示名を保存

        return redirect('accounts:login')

    return render(request, 'ongaku/register.html')

def register(request):
    """ユーザー登録ビュー"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 新しいユーザーを保存
            user = form.save()
            # ユーザーを自動的にログイン
            login(request, user)
            return redirect('profile')  # プロフィールページにリダイレクト
    else:
        form = RegisterForm()

    return render(request, 'ongaku/register.html', {'form': form})

def get_user_display_name(self, obj):
    try:
        # UserProfileが存在するか確認して、そのdisplay_nameを取得
        return obj.user.userprofile.display_name if obj.user.userprofile and obj.user.userprofile.display_name else obj.user.username
    except UserProfile.DoesNotExist:
        # UserProfileが存在しない場合は、usernameを返す
        return obj.user.username


def recommended_music(request):
    # 再生回数が多い順に取得（上位5件）
    recommended = Ongaku.objects.filter(play_count__gt=0).order_by('-play_count')[:10]
    return render(request, 'recommended_music.html', {'recommended': recommended})

# 定数としてのカテゴリーリスト
COMMON_CATEGORIES = [
    "ポップ", "ロック", "ジャズ", "クラシック", "エレクトロニカ",
    "ヒップホップ", "R&B", "カントリー", "ブルース", "その他"
]


def music_list(request):
    # フィルタリングされたカテゴリー
    selected_category = request.GET.get('category', '')

    # 曲データからカテゴリーを動的に取得（未登録の曲があれば"その他"に分類）
    categories = []
    for category in COMMON_CATEGORIES:
        music_count = Ongaku.objects.filter(category=category).count()
        categories.append({
            'name': category,
            'count': music_count,
        })

    # フィルタリング
    if selected_category and selected_category != "すべてのカテゴリー":
        musics = Ongaku.objects.filter(category=selected_category)
    else:
        musics = Ongaku.objects.all()

    return render(request, 'music_list.html', {
        'categories': categories,
        'musics': musics,
        'selected_category': selected_category,
    })

def increment_play_count(request, pk):
    if request.method == 'POST':
        try:
            ongaku = Ongaku.objects.get(pk=pk)
            ongaku.play_count += 1
            ongaku.save()
            return JsonResponse({'success': True, 'play_count': ongaku.play_count})
        except Ongaku.DoesNotExist:
            return JsonResponse({'success': False, 'error': '音楽が見つかりませんでした'}, status=404)
    return JsonResponse({'success': False, 'error': '無効なリクエスト'}, status=400)


def update_play_count(request, song_id):
    if request.method == "POST":
        song = get_object_or_404(Ongaku, id=song_id)
        song.play_count += 1
        song.save()
        return JsonResponse({'play_count': song.play_count})

def add_ongaku(request):
    if request.method == 'POST':
        form = OngakuForm(request.POST, request.FILES)  # request.FILESも追加
        if form.is_valid():
            # フォームの保存
            ongaku = form.save(commit=False)
            ongaku.user = request.user  # ユーザーを保存
            ongaku.save()
            return redirect('success_url')  # 成功後のリダイレクト
    else:
        form = OngakuForm()
    
    return render(request, 'add_ongaku.html', {'form': form})


# Create your views here.
# def search_view(request):
#     search_results = Song.objects.filter(title__icontains='検索キーワード')  # 例: データベースから曲を検索
#     return render(request, 'ongaku/search_results.html', {'search_results': search_results})


def search_view(request):
    query = request.GET.get('query', '')
    
    if query:
        search_results = Ongaku.objects.filter(
            Q(title__icontains=query) |
            Q(category__icontains=query) |
            Q(custom_category__icontains=query) |
            Q(user__username__icontains=query) |  # username での検索
            Q(user__userprofile__display_name__icontains=query)   # display_name での検索
        ).annotate(
            match_count=Count('title')
        ).order_by('-match_count')
    else:
        search_results = []

    search_history = request.session.get('search_history', [])
    if query and query not in search_history:
        search_history.append(query)
        request.session['search_history'] = search_history

    if query:
        for song in search_results:
            song.search_count += 1
            song.save()

    # おすすめ曲の取得
    recommended_songs = []
    if search_history:
        recommended_songs = Ongaku.objects.filter(
            title__icontains=search_history[-1]
        ).exclude(search_count=0)[:5]
    
    # ランダムな曲の取得
    random_songs = Ongaku.objects.exclude(search_count=0).order_by('?')[:5] if not recommended_songs else []

    return render(request, 'ongaku/search_results.html', {
        'search_results': search_results,
        'query': query,
        'recommended_songs': recommended_songs,
        'random_songs': random_songs,
        'search_history': search_history,
    })

def delete_history(request):
    if request.method == "POST":
        history_item = request.POST.get('history_item')
        search_history = request.session.get('search_history', [])
        if history_item in search_history:
            search_history.remove(history_item)
        request.session['search_history'] = search_history
    return redirect('search')

@login_required
def ongaku_detail(request, pk):
    """音楽詳細ページ"""
    ongaku = get_object_or_404(Ongaku, pk=pk)
    
    # 音楽オブジェクトに関連するフォルダを取得
    folders = Folder.objects.filter(song=ongaku)
    
    # お気に入り状態をチェック
    is_favorited = False
    if request.user.is_authenticated:
        user_profile = request.user.userprofile
        is_favorited = ongaku in user_profile.favorite_songs.all()
        print(f"お気に入り状態: {is_favorited}")  # ログに出力

    # コンテキストに渡す
    context = {
        'ongaku': ongaku,
        'folders': folders,
        'is_favorited': is_favorited,
    }
    
    return render(request, 'ongaku/ongaku_detail.html', context)


@login_required
def detail_view(request, pk):
    """音楽の詳細ページ"""
    object = get_object_or_404(Ongaku, pk=pk)

    # お気に入り状態を判定
    is_favorited = request.user in object.favorited_by.all()

    # コンテキストに情報を渡す
    context = {
        'object': object,
        'is_favorited': is_favorited,  # お気に入り状態
        'user': request.user,  # ログイン中のユーザー
    }
    return render(request, 'ongaku/detail.html', context)


class YourModelDetailView(DetailView):
    model = YourModel
    template_name = 'your_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # ログイン中のユーザーを渡す
        return context

def restricted_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')

    # オブジェクトを取得し、存在しない場合は404エラー
    obj = get_object_or_404(YourModel, pk=pk)

    # アクセス権限のチェック（カスタムロジック）
    if not request.user.has_perm('ongaku.can_view_restricted_content') and not request.user == obj.owner:
        return HttpResponseForbidden('アクセス権限がありません')

    # 必要な情報をコンテキストに追加
    context = {'object': obj}
    return render(request, 'restricted.html', context)



def index_view(request):
    # 音楽のリストを取得
    if request.user.is_authenticated:
        # ログインユーザーの場合、自分の曲はすべて表示、それ以外は公開曲のみ
        music_list = Ongaku.objects.filter(is_public=True) | Ongaku.objects.filter(user=request.user)
    else:
        # 未ログインユーザーは公開曲のみ
        music_list = Ongaku.objects.filter(is_public=True)

    # 新しい順に並べたリスト
    object_list = Ongaku.objects.order_by('-id')

    # 再生回数が多いトップ10
    recommended = Ongaku.objects.all().order_by('-play_count')[:10]

    # 平均評価でランキング
    ranking_list = Ongaku.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')

    # ページネーションの設定
    paginator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(
        request,
        'ongaku/index.html',
        {
            'music_list': music_list,
            'object_list': object_list,
            'recommended': recommended,
            'ranking_list': ranking_list,
            'page_obj': page_obj,
        },
    )

class ListOngakuView(LoginRequiredMixin, ListView):
    template_name = 'ongaku/ongaku_list.html'
    model = Ongaku
    paginated_by = ITEM_PER_PAGE

class DetailOngakuView(LoginRequiredMixin, DetailView):
    template_name = 'ongaku/ongaku_detail.html'
    model = Ongaku

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ongaku = context['ongaku']

        # 曲のお気に入り登録者数
        favorite_count = ongaku.favorites.count()

        # ユーザーがその曲をお気に入りに登録しているか
        is_favorited = self.request.user.favorite_songs.filter(id=ongaku.id).exists()

        context['favorite_count'] = favorite_count
        context['is_favorited'] = is_favorited
        return context



class CreateOngakuView(LoginRequiredMixin, CreateView):
    template_name = 'ongaku/ongaku_create.html'
    model = Ongaku
    fields = ('title', 'text', 'thumbnail', 'category', 'audio_file', 'custom_category', 'ongaku_url', 'is_public')
    success_url = reverse_lazy('list-ongaku')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    

    def create_ongaku(request):
        if request.method == 'POST':
            form = OngakuForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        else:
            form = OngakuForm()

        # 最新の音楽データを取得（例）
        ongaku = Ongaku.objects.last()  # 最後の音楽を取得（例）

        return render(request, 'ongaku/create_ongaku.html', {'form': form, 'ongaku': ongaku})

    
class DeleteOngakuView(LoginRequiredMixin, DeleteView):
    template_name = 'ongaku/ongaku_confirm_delete.html'
    model = Ongaku
    success_url = reverse_lazy('list-ongaku')

    def has_delete_permission(self, obj):
        return obj.user == self.request.user

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.has_delete_permission(obj):
            return render(self.request, 'error_page.html', {'message': 'この操作は無効です。'})
        return obj

class UpdateOngakuView(LoginRequiredMixin, UpdateView):
    model = Ongaku
    fields = ('title', 'text', 'thumbnail', 'category', 'audio_file', 'custom_category', 'ongaku_url', 'is_public')
    template_name = 'ongaku/ongaku_update.html'

    def update_ongaku(request, pk):
        ongaku = get_object_or_404(Ongaku, pk=pk)

        if request.method == 'POST':
            form = OngakuForm(request.POST, request.FILES, instance=ongaku)
            if form.is_valid():
                form.save()
                return redirect('detail-ongaku', pk=ongaku.pk)
        else:
            form = OngakuForm(instance=ongaku)

        return render(request, 'ongaku_update.html', {'form': form})
    
    def get_object(self, queryset=None):
        
        obj = super().get_object(queryset)

        if obj.user != self.request.user:
            raise PermissionDenied
        
        return get_object_or_404(Ongaku, pk=self.kwargs['pk'])
    
    def get_success_url(self):
        return reverse('detail-ongaku', kwargs={'pk': self.object.id})

class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ('ongaku', 'title', 'text', 'rate')
    template_name = 'ongaku/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ongaku'] = Ongaku.objects.get(pk=self.kwargs['ongaku_id'])
        
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-ongaku', kwargs={'pk': self.object.ongaku.id})
    
class OngakuDetailView(DetailView):
    model = Ongaku
    template_name = 'ongaku_detail.html'  # テンプレート名
