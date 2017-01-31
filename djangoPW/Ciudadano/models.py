from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import User
from Partido.models import Partido
from Circunscripcion.models import Circunscripcion

# Create your models here.


@python_2_unicode_compatible
class Ciudadano(User):
	DNI = models.CharField(max_length=9,unique=True)
	ciudad = models.CharField(max_length=200)
	codigoPostal = models.IntegerField()
	mesa = models.CharField(max_length=200)
	circunscripcion = models.ForeignKey(Circunscripcion)
	votado = models.BooleanField(default=False)
	def __str__(self):
		return self.username

@python_2_unicode_compatible
class Candidato(Ciudadano):
	imagen = models.CharField(max_length=200)
	partido = models.ForeignKey(Partido, null=True, related_name="candidato")
	def __str__(self):
		return self.username
	
