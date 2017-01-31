from django.forms.extras.widgets import SelectDateWidget
from django.forms import ModelForm
from django import forms
from Ciudadano.models import Ciudadano,Candidato
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class crearCiudadanoForm(UserCreationForm):
	class Meta:
		model = Ciudadano
		fields = ('first_name','last_name','DNI','ciudad','codigoPostal','mesa','circunscripcion','username')

class crearCandidatoForm(UserCreationForm):
	class Meta:
		model = Candidato
		fields = ('first_name','last_name','DNI','ciudad','codigoPostal','mesa','partido','imagen','circunscripcion','username')

class editarCandidatoForm(ModelForm):
	class Meta:
		model = Candidato
		
		fields = ('first_name','last_name','DNI','ciudad','codigoPostal','mesa','partido','imagen','circunscripcion')

class editarCiudadanoForm(ModelForm):
	class Meta:
		model = Ciudadano
		
		fields = ('first_name','last_name','DNI','ciudad','codigoPostal','mesa','circunscripcion')
		
class addCandidatoForm(UserCreationForm):
	class Meta:
		model = Candidato
		fields = ('first_name','last_name','DNI','ciudad','codigoPostal','mesa','imagen','circunscripcion','username')

class loginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput, label="Password")

class ElegirCiudadanoForm(forms.Form):
	imagen = forms.CharField()
	seleccionar_ciudadano = forms.ModelChoiceField(queryset=Ciudadano.objects.all())
	
class CambiarContraseniaForm(forms.Form):
	password_actual=forms.CharField(widget= forms.PasswordInput, label="Password actual")
	password=forms.CharField(widget=forms.PasswordInput, label="Nueva password")
	password_check=forms.CharField(widget= forms.PasswordInput, label="Repetir nueva password")
