from django import forms
from .models import Post
from tinymce.widgets import TinyMCE

class PostForm(forms.ModelForm):
    # title = forms.CharField(max_length=165,)
    # body = forms.Textarea()

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': TinyMCE()
        }
        exclude = ['user', 'created_at']