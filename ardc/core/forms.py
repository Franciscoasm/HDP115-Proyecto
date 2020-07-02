from django import forms

from .models import Departamento, Municipio, Beneficio, Benefactor


class FormFiltrar(forms.Form):

    departamento = forms.ModelChoiceField(
        label=u'', 
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
    )
    
    municipio = forms.ModelChoiceField(
        label=u'', 
        queryset=Municipio.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
    )

    ayudas = forms.ModelChoiceField(
        label=u'', 
        queryset=Beneficio.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
    )

    entidades = forms.ModelChoiceField(
        label=u'', 
        queryset=Benefactor.objects.all(),
        widget=forms.Select(attrs={'class':'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super(FormFiltrar, self).__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()