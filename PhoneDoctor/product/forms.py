from django import forms
from .models import Product,Brand,Category

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

class NewCategoryForm(forms.ModelForm):
     class Meta:
        model = Category
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
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