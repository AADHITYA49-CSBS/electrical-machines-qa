from django import forms


class QuestionForm(forms.Form):
    question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "rows": 5,
                "placeholder": "Ask about transformers, motors, generators, alternators...",
                "class": "form-control form-control-lg",
                "aria-label": "Ask ElectraMind AI"
            }
        )
    )