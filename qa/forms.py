from django import forms


class QuestionForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Ask about electrical machines..."
            }
        )
    )