from django.http import HttpResponse
from django.utils import timezone 
from Partido.models import Partido
from Ciudadano.models import Ciudadano, Candidato
from Circunscripcion.models import Circunscripcion, Voto_partido_circu
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy


#Funcion para ver la pagina principal
def index(request):
	return render(request,'djangoPW/index.html')

