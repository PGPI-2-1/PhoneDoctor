from django import forms
from .models import Reclamacion

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewReclamacionForm(forms.ModelForm):
     class Meta:
        model = Reclamacion
        fields = ('descripcion',)
        widgets = {
            'description': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
         }