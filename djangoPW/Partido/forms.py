from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm
from django import forms
from Partido.models import Partido
from Circunscripcion.models import Circunscripcion

class ModificarPartidoForm(ModelForm):
	class Meta:
		model = Partido
		
		fields = ('nombre','anioCreacion','breveHistoria','programaElectoral','imagen')
		
class crearPartidoForm(ModelForm):
	class Meta:
		model = Partido
		fields = ('__all__')
		
	circunscripcion = forms.ModelChoiceField(queryset=Circunscripcion.objects.all())

class AgregarCircunscripcion(forms.Form):
	selecciona_la_circunscripcion = forms.ModelChoiceField(queryset=Circunscripcion.objects.all())

