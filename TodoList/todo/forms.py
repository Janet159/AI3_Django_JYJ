# todo/forms.py
from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 30자 이하로 입력해주세요.',
                'maxlength': '30',
                'autofocus': True,
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '내용을 입력해주세요. (선택)',
                'rows': 3,
            }),
        }
        error_messages = {
            'title': {
                'required': '제목은 필수 입력입니다.',
                'max_length': '제목은 30자 이하로 입력해주세요.',
            },
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError("제목이 비어 있습니다.")
        if len(title) > 30:
            raise forms.ValidationError("제목은 30자 이하로 입력해주세요.")
        return title
