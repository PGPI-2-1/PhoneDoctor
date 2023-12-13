from django import forms
from .models import Product,Brand,Category, Opinion

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewBrandForm(forms.ModelForm):
     class Meta:
        model = Brand
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

        labels = {
            'name': 'Nombre:',
        }

class NewCategoryForm(forms.ModelForm):
     class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }
        labels = {
            'name': 'Nombre:',
        }
              
class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('brand','category','name','description','price','quantity','image',)

        widgets = {
            'brand': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'quantity': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

        labels = {
            'brand': 'Marca:',
            'category': 'Categoría:',
            'name': 'Nombre:',
            'description': 'Descripción:',
            'price': 'Precio:',
            'image': 'Imagen:',
            'quantity': 'Cantidad:',
        }

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('brand','category','name','description','price','quantity','image',)

        widgets = {
            'brand': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
            'quantity': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

        labels = {
            'brand': 'Marca:',
            'category': 'Categoría:',
            'name': 'Nombre:',
            'description': 'Descripción:',
            'price': 'Precio:',
            'image': 'Imagen:',
            'quantity': 'Cantidad:',
        }

class NewOpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ('valoracion','description')

        widgets = {
            'valoracion': forms.NumberInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
        }

        labels = {
            'valoracion': 'Valoración:',
            'description': 'Descripción:',
        }
