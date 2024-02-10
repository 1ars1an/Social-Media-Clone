from django import forms

class CreatePost(forms.Form):
    content = forms.CharField(label="Create Your Post!" ,max_length=180, widget=forms.Textarea)