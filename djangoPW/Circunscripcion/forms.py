from django import forms
from django.forms import ModelForm
from Circunscripcion.models import Circunscripcion
from Partido.models import Partido

class crearCircunscripcionForm(forms.Form):
	nombre = forms.CharField()
	selecciona_un_partido = forms.ModelChoiceField(queryset=Partido.objects.all())
	
class crearCircunscripcionYPartidoForm(ModelForm):
	class Meta:
		model = Partido
		fields = ('__all__')
	
	nombre_circunscripcion = forms.CharField()	
	
class votarForm(forms.Form):
	partidos = forms.ModelChoiceField(queryset=Partido.objects.all())
	
		
	
