from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

class CreatePost(forms.Form):
    content = forms.CharField(max_length=180, widget=forms.Textarea(attrs={'class': 'w-50 form-control form-control-sm', 'placeholder': 'Max: 180 Chars!'}), validators=[MinLengthValidator(15, "The post must be at least 15 chars long"), MaxLengthValidator(180, "The post cannot exceed 180 chars")])