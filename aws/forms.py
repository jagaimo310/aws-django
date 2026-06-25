from django import forms

class prompt_form(forms.Form):
    prompt = forms.CharField(label = "",
                             widget=forms.Textarea(
                                attrs={
                                    "placeholder": "生成したい画像を教えてください",
                                    "rows": 5,
                                    "cols": 50,
                                    "class": "my-textarea-class",
                                }
                             ),max_length=500,required=True)