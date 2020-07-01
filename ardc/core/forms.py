from django import forms

from agregar.models import Departamento, Municipio


class UbicacionForm(forms.Form):

    departamento = forms.ModelChoiceField(
        label=u'', 
        queryset=Departamento.objects.all()
    )
    
    municipio = forms.ModelChoiceField(
        label=u'', 
        queryset=Municipio.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(UbicacionForm, self).__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()