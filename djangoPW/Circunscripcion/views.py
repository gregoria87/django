from django.shortcuts import render
from Circunscripcion.models import Circunscripcion, Voto_partido_circu
from Partido.models import Partido
from Ciudadano.models import Ciudadano, Candidato
from django.http import HttpResponse
from django.utils import timezone 
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from Circunscripcion.forms import crearCircunscripcionForm, crearCircunscripcionYPartidoForm, votarForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

#Funcion para votar
@login_required(login_url='Ciudadano:entrar')
def votar(request):
	ciudadano = get_object_or_404(Ciudadano,username=request.user.get_username())
	if ciudadano.votado == False:
		if request.method == 'POST':
			form = votarForm(request.POST)
			opcion = request.POST['partidos']
			partido = get_object_or_404(Partido,id=opcion)
			existe_relacion = Voto_partido_circu.objects.filter(partido=partido,circunscripcion=ciudadano.circunscripcion)
			if existe_relacion:
				relacion = Voto_partido_circu.objects.get(partido=partido,circunscripcion=ciudadano.circunscripcion)
				relacion.votos = relacion.votos+1
				ciudadano.votado = True
				ciudadano.save()
				relacion.save()
				mensaje = "Su voto se ha registrado correctamente"
				context = {'mensaje':mensaje}
				return render(request,'djangoPW/index.html',context)
			else:
				mensaje = "Ese partido no se presenta a tu circunscripcion. Elige otro porfavor."
				context ={'form':form,'mensaje':mensaje}
			return render(request,'Circunscripcion/votar.html',context)
		else:
			form = votarForm()
		context ={'form':form}
		return render(request,'Circunscripcion/votar.html',context)
	else:
		mensaje = "Ya ha votado, no puede volver a votar"
	context={'mensaje':mensaje}
	return render(request,'djangoPW/index.html',context)

#Funcion para ver los resultados de las elecciones tanto durante el proceso electoral como al finalizar este, ya que no se ha considerado una fecha de finalizacion del proceso.
def verResultados(request):
	partidos = Partido.objects.all()
	vectorVotos = []
	vectorEscanios = []
	votosTotales = 0
	escaniosAsignados = 0
	repartidos = []
	if partidos:
		for partido in partidos:
			relacion_circu = Voto_partido_circu.objects.filter(partido=partido)
			votos = 0
			for relacion in relacion_circu:
				votos = votos+relacion.votos
			votosTotales = votosTotales+votos
			tuplaVotos=(partido,votos)
			vectorVotos.append(tuplaVotos)
		if votosTotales > 0: #Si hay votos, los repartimos en escanios
			for tuplaVotos in vectorVotos:
				escanios=(tuplaVotos[1]*100)/votosTotales
				nuevaTupla=(tuplaVotos[0],escanios)
				vectorEscanios.append(nuevaTupla)
				escaniosAsignados = escaniosAsignados+escanios
				repartidos.append(escanios)
			escaniosSobrantes = 100 - escaniosAsignados #Asignamos al partido con mas escanios los sobrantes tambien
			escaniosGanador=max(repartidos)
			for i in range(0,len(repartidos)-1):
				if escaniosGanador == repartidos[i]:
					break
			partido=vectorEscanios[i][0]
			del vectorEscanios[i]
			nuevaTupla=(partido,escaniosGanador+escaniosSobrantes)
			vectorEscanios.append(nuevaTupla)
		else:
			vectorEscanios = vectorVotos #Cuando todavia no ha votado nadie, es decir, todos tienes votos = 0, no se reparten escanios	
	context={'vector':vectorEscanios}
	return render(request,'Circunscripcion/verResultados.html',context)
		
#Funcion para crear una circunscripcion, creando tambien la relacion circunscripcion-partido
@staff_member_required
def crearCircunscripcion(request):
	mensaje = None
	partidos = Partido.objects.all() #Si existen partidos seleccionamos uno de los existentes y sino lo creamos tambien
	if partidos.count():
		if request.method == 'POST':
			form = crearCircunscripcionForm(request.POST)
			if form.is_valid():
				nombre = request.POST['nombre']
				if Circunscripcion.objects.filter(nombre=nombre).count():
					mensaje = "Ya existe una circunscripcion con ese nombre, elige otro por favor."
					context = {'form':form,'mensaje':mensaje}
					return render(request,'Circunscripcion/crearCircunscripcion.html',context)
				else:
					opcion = request.POST['selecciona_un_partido']
					partido = get_object_or_404(Partido, id=opcion)
					c=Circunscripcion(nombre=nombre) #Guardamos la Circunscripcion
					c.save()
					relacion = Voto_partido_circu(circunscripcion=c,partido=partido) #Creamos la relacion entre ellos
					relacion.save()
					return redirect('Circunscripcion:mostrarCircunscripciones')
			else:
				mensaje = "No ha rellenado correctamente el formulario"
			context = {'form':form,'mensaje':mensaje}
			return render(request,'Circunscripcion/crearCircunscripcion.html',context)
		else:
			form = crearCircunscripcionForm()
		context = {'form':form}
		return render(request,'Circunscripcion/crearCircunscripcion.html',context)
	else:
		if request.method == 'POST':
			form = crearCircunscripcionYPartidoForm(request.POST)
			if form.is_valid():
				nombreCircunscripcion = request.POST['nombre_circunscripcion']
				nombre = request.POST['nombre']
				anio = request.POST['anioCreacion']
				breveHistoria = request.POST['breveHistoria']
				programa = request.POST['programaElectoral']
				imagen = request.POST['imagen']
				partido = Partido(nombre=nombre,anioCreacion=anio,breveHistoria=breveHistoria,programaElectoral=programa,imagen=imagen)
				partido.save() #Guardamos el partido
				c=Circunscripcion(nombre=nombreCircunscripcion) #Guardamos la Circunscripcion
				c.save()
				relacion = Voto_partido_circu(circunscripcion=c,partido=partido) #Creamos la relacion entre ellos
				relacion.save()
				return redirect('Circunscripcion:mostrarCircunscripciones')
			else:
				mensaje = "No ha rellenado correctamente el formulario"
			context = {'form':form,'mensaje':mensaje}
			return render(request,'Circunscripcion/crearCircunscripcion.html',context)
		else:
			form = crearCircunscripcionYPartidoForm()
		context = {'form':form}
		return render(request,'Circunscripcion/crearCircunscripcion.html',context)
		
		
	
#Funcion para borrar una circunscripcion, teniendo en cuenta que al borrar la circunscripcion se borraran los ciudadanos asociados a esta, ya que deben pertenecer obligatoriamente a una unica circunscipcion
class borrarCircunscripcion(DeleteView):
	model = Circunscripcion
	context_object_name = 'circunscripcion'
	template_name="Circunscripcion/borrarCircunscripcion.html"
	success_url = reverse_lazy('index')
	

#Funcion para ver todas las circunscripciones
class verCircunscripciones(ListView):
	model = Circunscripcion
	context_object_name = 'circunscripciones'
	template_name = 'Circunscripcion/mostrarCircunscripciones.html'
	
	def get_queryset(self):
		return Circunscripcion.objects.all()

#Funcion para ver una circunscripcion en detalle
def verCircunscripcionDetalle(request,circunscripcion_id):
	circunscripcion = get_object_or_404(Circunscripcion,id=circunscripcion_id)
	relacion_partidos_circunscripcion = Voto_partido_circu.objects.filter(circunscripcion=circunscripcion)
	ciudadanos = Ciudadano.objects.filter(circunscripcion=circunscripcion_id)
	context = {'relacion_partidos_circunscripcion':relacion_partidos_circunscripcion,'circunscripcion':circunscripcion,'ciudadanos':ciudadanos}
	return render(request,'Circunscripcion/verCircunscripcionDetalle.html',context)
	
#Funcion para editar una circunscripcion
class modificarCircunscripcion(UpdateView):
	model = Circunscripcion
	fields = ['nombre']
	template_name = 'Circunscripcion/modificarCircunscripcion.html'
	success_url = reverse_lazy('Circunscripcion:mostrarCircunscripciones')

