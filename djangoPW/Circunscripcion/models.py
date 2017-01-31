from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from Partido.models import Partido

# Create your models here.

@python_2_unicode_compatible
class Circunscripcion(models.Model):
	nombre = models.CharField(max_length=50,unique=True)
	partido = models.ManyToManyField(Partido,through="Voto_partido_circu")
	def __str__(self):
		return self.nombre

#@python_2_unicode_compatible	
class Voto_partido_circu(models.Model):
	votos = models.IntegerField(default=0)
	circunscripcion = models.ForeignKey(Circunscripcion)
	partido = models.ForeignKey(Partido)
	#def __str__(self):
	#	return self.votos
	
