from django import forms

from .models import Post, Comment

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class SignUpForm(UserCreationForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name=forms.CharField(max_length=103,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name=forms.CharField(max_length=103,widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model= User
        fields=('username','first_name','last_name','email','password1','password2')

    def __init__(self,*args,**kwargs):
        super(SignUpForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['class']='form-control'


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # fields that i want to be edit
        fields = ('author','title', 'text',)
        # pass widget attribute to the meta class
        # grab widget for particular
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'author': forms.TextInput(attrs={'class': 'textinputclass', 'id':'user','value':'','type':'hidden'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(CommentForm, self).__init__(*args, **kwargs)
    #     self.fields['author'].widget.attrs['readonly'] = True
    class Meta:
        model = Comment
        fields = ( 'text',)
        # author=forms.ChoiceField(queryset=Post.object.all())

        widgets = {
            'author': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
