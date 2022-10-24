from django import forms
from .models import Comment

# 新建一个表单
# form.Form 建立一个标准的表单
# from.Model_form 建一个与model有关的表单
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=20, label='当前用户')
    email = forms.EmailField(label='发送人邮箱')
    to = forms.EmailField(label='收件人邮箱')
    

    # 值非法时，将不报错，而是将值置为空，部件修改为textarea，替换默认的input框
    comments = forms.CharField(required=False,
                               widget=forms.Textarea,
                               label='评论')

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment  # 指定对应的model
        fields = ('name', 'email', 'body')  # 展示在前端，需要用户填写的字段
        

# 搜索视图
class SearchForm(forms.Form):
    query = forms.CharField(label='搜索')