from django import forms

from agregar.models import Departamento, Municipio


class UbicacionForm(forms.Form):

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

    def __init__(self, *args, **kwargs):
        super(UbicacionForm, self).__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()