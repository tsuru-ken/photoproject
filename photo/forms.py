from django.forms import ModelForm

from .models import PhotoPost

class PhotoPostForm(ModelForm):
    '''ModelFormのサブクラス'''
    
    class Meta:
        '''ModelFormクラスのインナークラス
        
        Attributes:
        model:モデルのクラス
        fields:フォームで使用するモデルのフィールドを指定
        '''
        model = PhotoPost
        fields =['category','title','comment','image1','image2']