from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from .models import YourModel
from django.db.models import Avg, F, Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from .forms import OngakuForm
from .models import Ongaku, Review, Category
from .consts import ITEM_PER_PAGE
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView
    )

def recommended_music(request):
    # 再生回数が多い順に取得（上位5件）
    recommended = Ongaku.objects.filter(play_count__gt=0).order_by('-play_count')[:10]
    return render(request, 'recommended_music.html', {'recommended': recommended})

# 定数としてのカテゴリーリスト
COMMON_CATEGORIES = [
    "ポップ", "ロック", "ジャズ", "クラシック", "エレクトロニカ",
    "ヒップホップ", "R&B", "カントリー", "ブルース", "その他"
]


def create_ongaku(request):
    if request.method == "POST":
        form = OngakuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('some_success_page')
    else:
        form = OngakuForm()
    return render(request, 'ongaku/create_ongaku.html', {'form': form})


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
    search_results1 = Ongaku.objects.filter(Q(title__icontains=query) | Q(category__icontains=query)) if query else []
    
    # 検索履歴をセッションに保存
    search_history = request.session.get('search_history', [])
    if query and query not in search_history:
        search_history.append(query)
        request.session['search_history'] = search_history  # セッションを更新
    
    search_results1 = Ongaku.objects.filter(Q(title__icontains=query)| Q(category__icontains=query)).annotate(
    match_count=Count('title')
    ).order_by('-match_count') if query else []

    # 検索回数のカウントアップ
    if query:
        for song in search_results1:
            song.search_count += 1
            song.save()

    # おすすめ曲の取得（検索回数が0回のものを除外）
    if search_history:
        recommended_songs = Ongaku.objects.filter(
            title__icontains=search_history[-1]
        ).exclude(search_count=0)[:5]
    else:
        recommended_songs = []
    
    # おすすめ曲がない場合、ランダムな曲を取得（検索回数が0回のものを除外）
    if not recommended_songs:
        random_songs = Ongaku.objects.exclude(search_count=0).order_by('?')[:5]  # ランダムに5曲を表示
    else:
        random_songs = []

    return render(request, 'ongaku/search_results.html', {
        'search_results': search_results1,
        'query': query,
        'recommended_songs': recommended_songs,
        'random_songs': random_songs,
        'search_history': search_history,
    })

    # query = request.GET.get('query', '')  # クエリパラメータを取得
    # ongakus = Ongaku.objects.all()  # 初期状態では全ての曲を取得

    # # クエリが入力されている場合、タイトルやカテゴリでフィルタリング
    # if query:
    #     ongakus = ongakus.filter(Q(title__icontains=query) | Q(category__icontains=query))

    # # ページネーション
    # paginator = Paginator(ongakus, 10)  # 1ページに10件表示
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # # 人気の曲を取得（例として、検索回数が多い曲を表示）
    # popular_songs = Ongaku.objects.annotate(
    #     annotated_search_count=F('search_count')
    # ).order_by('-annotated_search_count')[:5]

    # return render(request, 'ongaku/search_results.html', {
    #     'form': SearchForm(),  # フォームをテンプレートに渡す場合
    #     'query': query,  # クエリパラメータをテンプレートに渡す
    #     'page_obj': page_obj,  # ページネーション用のオブジェクト
    #     'popular_songs': popular_songs,  # 人気の曲
    # })
    

def detail_view(request, pk):
    object = get_object_or_404(Ongaku, pk=pk)
    return render(request, 'ongaku/detail.html', {'object': object})

def ongaku_detail(request, pk):
    ongaku = get_object_or_404(Ongaku, pk=pk)
    context = {'ongaku': ongaku}
    return render(request, 'ongaku/ongaku_detail.html', context)


def delete_history(request):
    if request.method == "POST":
        history_item = request.POST.get('history_item')
        search_history = request.session.get('search_history', [])
        if history_item in search_history:
            search_history.remove(history_item)
        request.session['search_history'] = search_history
    return redirect('search')


@login_required
def detail_view(request, pk):
    obj = get_object_or_404(YourModel, pk=pk)
    return render(request, 'your_template.html', {
        'object': obj,
        'user': request.user,  # ログイン中のユーザーを渡す
    })

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
    music_list = Ongaku.objects.all()

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

class CreateOngakuView(LoginRequiredMixin, CreateView):
    template_name = 'ongaku/ongaku_create.html'
    model = Ongaku
    fields = ('title', 'text', 'thumbnail', 'category', 'audio_file')
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

        return render(request, 'create_ongaku.html', {'form': form, 'ongaku': ongaku})

    
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
    fields = ('title', 'text', 'thumbnail', 'category', 'audio_file')
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
