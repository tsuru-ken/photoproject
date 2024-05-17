from django.contrib import admin

# CustomUserをインポート
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    # 管理ページのレコード一覧に表示するカラムを設定するクラス

    # レコードと一緒にidとusernameを表示（タプル）
    list_display = ('id', 'username')

    # 表示するカラムにリンクを設定
    list_display_links = ('id','username')


admin.site.register(CustomUser, CustomUserAdmin)