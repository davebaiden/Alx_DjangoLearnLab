from django import forms
from .models import Post, Comment, Tag

class PostForm(forms.ModelForm):
    # a simple text input for tags (comma-separated)
    tags = forms.CharField(required=False, help_text='Comma-separated tags', 
                           widget=forms.TextInput(attrs={'placeholder': 'e.g. django, python'}))

    class Meta:
        model = Post
        fields = ['title', 'content']  # tags handled separately
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post here...', 'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        # populate initial tags string when editing existing post
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags'].initial = ', '.join([t.name for t in self.instance.tags.all()])

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write a comment...', 'rows': 4}),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content
