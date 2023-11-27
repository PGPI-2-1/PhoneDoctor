from django import forms
from .models import Review

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'
              
class NewReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title','description')

        widgets = {
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            })
        }