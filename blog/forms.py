from blog.models import Post
from django import forms


class BookForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['book_author', 'title', 'text', 'img']



