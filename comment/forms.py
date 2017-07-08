from django import forms
from .models import Comment
from django.utils import timezone

Grade_Choices = [(i, str(i)) for i in range(1, 6)]

class CommentForm(forms.Form):
        name = forms.CharField()
        body = forms.CharField()
        grade = forms.TypedChoiceField(choices=Grade_Choices, coerce=int)


class ReplyForm(forms.Form):
        reply = forms.CharField()
