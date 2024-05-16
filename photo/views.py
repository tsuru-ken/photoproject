from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render



# django.views.genericからTemplateView,ListViewをインポート
from django.views.generic import TemplateView,ListView

# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView

# django.urlsからreverse_lazyをインポート
from django.urls import reverse_lazy

# formsモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm

# method_decoratorをインポート
from django.utils.decorators import method_decorator

# login_requiredをインポート
from django.contrib.auth.decorators import login_required

# modelモジュールからモデルPhotoPostモデルをインポート
from .models import PhotoPost

# django.views.genericからDetailViewをインポート
from django.views.generic import DetailView

# 
from django.views.generic import DeleteView

class IndexView(ListView):
    '''トップページのビュー'''

    # index.htmlをレンダリング
    template_name = 'index.html'
    
    # モデルBlogPostのオブジェクトにorder_by()を適用して
    # 投稿日時の降順で並べ替える
    queryset = PhotoPost.objects.order_by('-posted_at')
    
    # 1ページに表示するレコードの件数
    paginate_by = 9

# デコレータにより、CreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsetting.pyのLOGIN＿URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    
    '''写真投稿ページのビュー
    PhotoPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する。
    
    Attributes:
    form_class: モデルとフィールドが登録されたフォームクラス
    template_name: レンダリングするテンプレート
    success_url フォームデータ登録完了後のリダイレクト先'''
    
    # forms.pyのPhotoPostFormをフォームクラスとして登録
    form_class = PhotoPostForm
    
    # レンダリングするテンプレート
    template_name = "post_photo.html"
    
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')

    
    def form_valid(self, form):
        '''CreateViesクラスのform_validをオーバーライド
        フォームのバリデーションを通過した時に呼ばれる
        フォームデータの登録をここで行う
        
        parmeters:
            form(django.forms.Form):
                form_classに格納されているPhotoPostFormオブジェクト
        Return:
            HttpResponseRedirectオブジェクト:
                スパークラスのform_valid()の戻り値を返すことで、
                success_urlで設定されているURLにリダイレクトさせる
        
        
        '''
        # commit=FalseにしてPOSTされたデータを所得
        postdata = form.save(commit=False)
        
        # 投稿ユーザーのidを所得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        
        # 投稿データをデータベースに登録
        postdata.save()
        
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)


class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
    Attributes:
        template_name:レンダリングするテンプレート
    '''
    
    # index.htmlをレンダリングする
    template_name = 'post_success.html'
    
    
class CategoryView(ListView):
    '''カテゴリページのビュー
    Attributes:
        template_name: レンダリングするテンプレート
        paginete_by: 1ページに表示するレコードの件数
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    
    # 1ページに表示するレコードの件数
    paginate_by = 9
    
    
    def get_queryset(self):
        '''クエリを実行する
        self.kwargsの所得が必要なため、クラス変数quersetではなく、
        get_queryset()のオーバーライドによりクエリを実行する
        
        Returns:
            クエリによる所得されたレコード
        '''
        
        # self.kwargsでキーワードの辞書を所得し、
        # categoryキーの値(Categorysテーブルのid)を所得
        category_id = self.kwargs['category']
        
        # filter(フィールド名=id)で絞り込む
        categories = PhotoPost.objects.filter(
            category =category_id).order_by('-posted_at')
        # クエリによって所得されたレコードを返す
        return categories
    
    
class UserView(ListView):
    
    
    template_name ='index.html'
    
    paginate_by = 9
    
    def get_queryset(self):
        user_id = self.kwargs['user']
        
        user_list = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        
        return user_list
    

class DetailView(DetailView):
    
    template_name ='detail.html'
    
    model = PhotoPost
    
    
class MypageView(ListView):
    
    template_name ='mypage.html'
    
    paginate_by =9
    
    def get_queryset(self):
        queryset = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        
        return queryset


class PhotoDeleteView(DeleteView):
    model = PhotoPost
    
    template_name = 'photo_delete.html'
    
    success_url = reverse_lazy('photo:mypage')
    
    def delete(self, request, *args, **kwargs):
        
        return super().delete(request, *args, **kwargs)