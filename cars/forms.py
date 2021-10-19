from django import forms
from django.forms import ModelForm
from .models import Cars
from django.forms.widgets import NumberInput
from django import forms

#Create a Cars form
class CarsForm(ModelForm):
    class Meta:
        model = Cars
        fields = "__all__" #można zaimportować całośc

        widgets = {
            'mark' : forms.TextInput(attrs={'class':'form-control'}),
            'model' : forms.TextInput(attrs={'class':'form-control'}),
            'color' : forms.TextInput(attrs={'class':'form-control'}),
            'note' : forms.TextInput(attrs={'class':'form-control'}),
            }


class DateInput(forms.DateInput):
    input_type = 'date'

