from django.http import HttpResponse
from django.utils import timezone 
from Partido.models import Partido
from Ciudadano.models import Ciudadano, Candidato
from Circunscripcion.models import Circunscripcion, Voto_partido_circu
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from Ciudadano.forms import editarCiudadanoForm, editarCandidatoForm, addCandidatoForm, ElegirCiudadanoForm, loginForm, CambiarContraseniaForm, crearCandidatoForm, crearCiudadanoForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from urllib import quote_plus

# Create your views here.

#Funcion para ver los atributos de un candidato
class detallesCandidato(DetailView):
	model = Candidato
	template_name = 'Ciudadano/detallesCandidato.html'
	
#Funcion para ver los atributos de un ciudadano
class detallesCiudadano(DetailView):
	model = Ciudadano
	template_name = 'Ciudadano/detallesCiudadano.html'

#Agregar un candidato a un determinado partido desde detallesPartido (no puede seleccionar partido)
@login_required(login_url='Ciudadano:entrar')
def addCandidato(request, partido_id):
	mensaje = None
	partido= get_object_or_404(Partido, id=partido_id)
	if request.method == 'POST':
		form = addCandidatoForm(request.POST)
		last_name = request.POST['last_name']
		first_name = request.POST['first_name']
		username = request.POST['username']
		password = request.POST['password1']
		DNI = request.POST['DNI']
		mesa = request.POST['mesa']
		codigoPostal = request.POST['codigoPostal']
		ciudad = request.POST['ciudad']
		imagen = request.POST['imagen']
		opcion = request.POST['circunscripcion']
		if User.objects.filter(username=username).count():
			mensaje = "El usuario ya existe"
			context = {'mensaje': mensaje,'form': form}
			return render(request,'Ciudadano/addCandidatoPartido.html',context)
		else:
			if form.is_valid():
				circunscripcion = get_object_or_404(Circunscripcion,id=opcion)
				candidato = Candidato(first_name=first_name,last_name=last_name,username=username,password=password,DNI=DNI,mesa=mesa,codigoPostal=codigoPostal,ciudad=ciudad,imagen=imagen,partido=partido, circunscripcion=circunscripcion)
				candidato.save()
				return redirect('Partido:detallesPartido',partido_id)
			else:
				mensaje = "Formulario incorrecto"
			context = {'mensaje': mensaje,'form': form}
			return render(request,'Ciudadano/addCandidatoPartido.html',context)
	else:
		form = addCandidatoForm()
	context = {'form':form}
	return render(request,'Ciudadano/addCandidatoPartido.html',context)
	
#Funcion para seleccionar un ciudadano como candidato
@login_required(login_url='Ciudadano:entrar')
def addCiudadanoComoCandidato(request,partido_id):
	if request.user.is_staff or Candidato.objects.filter(partido = partido_id,username=request.user.username).count():
		if request.method == 'POST':
			form = ElegirCiudadanoForm(request.POST)
			if form.is_valid():
				imagen = request.POST['imagen']
				opcion = request.POST['seleccionar_ciudadano']
				c = get_object_or_404(Ciudadano,id=opcion)
				if Candidato.objects.filter(username=c.username): #Si el ciudadano ya es candidato de otro partido
					mensaje = "Ese ciudadano ya es candidato de otro partido"
					context={'form':form,'mensaje':mensaje}
					return render(request,'Ciudadano/seleccionarCiudadano.html',context)
				else:
					partido = get_object_or_404(Partido,id=partido_id)
					candidato = Candidato(first_name=c.first_name,last_name=c.last_name,username=c.username,password=c.password,DNI=c.DNI,mesa=c.mesa,codigoPostal=c.codigoPostal,ciudad=c.ciudad,imagen=imagen,partido=partido,circunscripcion=c.circunscripcion)
					c.delete()
					candidato.save()
				return redirect('Partido:detallesPartido', partido_id)
		else:
			form = ElegirCiudadanoForm()
		context={'form':form}
		return render(request,'Ciudadano/seleccionarCiudadano.html',context)
	else:
		mensaje = "No puedes agregar candidatos si no perteneces al partido"
		partido = get_object_or_404(Partido, id = partido_id)
		candidatos = Candidato.objects.filter(partido = partido_id)
		relacion_circunscripciones = partido.voto_partido_circu_set.all()
		context = {'mensaje':mensaje,'partido':partido,'candidatos':candidatos,'relacion_circunscripciones':relacion_circunscripciones}
		return render(request,'Partido/detallesPartido.html',context)
		
	
	
#Funcion para crear un nuevo ciudadano
@login_required(login_url='Ciudadano:entrar')
def crearCiudadano(request):
	if request.method == 'POST':
		form = crearCiudadanoForm(request.POST)
		if form.is_valid():
			DNI = request.POST['DNI']
			ciudadano = Ciudadano.objects.filter(DNI=DNI)
			if ciudadano.count():
				mensaje = "Ya existe un ciudadano con ese DNI."
				context={'form':form,'mensaje':mensaje}
				return render(request,'Ciudadano/crearCiudadano.html',context)
			else:
				form.save()
				return redirect('Ciudadano:verCiudadanos')
		else:
			context={'form':form}
			return render(request,'Ciudadano/crearCiudadano.html',context)
	else:
		form = crearCiudadanoForm()
	context={'form':form}
	return render(request,'Ciudadano/crearCiudadano.html',context)

#Funcion para crear un nuevo candidato
@login_required(login_url='Ciudadano:entrar')
def crearCandidato(request):
	if request.method == 'POST':
		form = crearCandidatoForm(request.POST)
		if form.is_valid:
			form.save()
			username = request.POST['username']
			candidato = get_object_or_404(Candidato,username=username)
			mensaje = "Candidato registrado correctamente"
			context={'mensaje':mensaje,'partido':candidato.partido}
			return render(request,'Partido/detallesPartido.html',context)
		else:
			context={'form':form}
			return render(request,'Ciudadano/crearCandidato.html',context)
	else:
		form = crearCandidatoForm()
	context={'form':form}
	return render(request,'Ciudadano/crearCandidato.html',context)

#Funcion para borrar un ciudadano
class borrarCiudadano(DeleteView):
	model = Ciudadano
	context_object_name = 'ciudadano'
	template_name="Ciudadano/borrarCiudadano.html"
	success_url = reverse_lazy('index')
	
#Funcion para borrar un candidato, teniendo en cuenta que se borra como candidato, pero no como ciudadano
@staff_member_required
def borrarCandidato(request,candidato_id):
	c = get_object_or_404(Candidato, id = candidato_id)
	if request.method == 'POST':
		partido = get_object_or_404(Partido, id = c.partido.id)
		ciudadano = Ciudadano(first_name=c.first_name,last_name=c.last_name,username=c.username,password=c.password,DNI=c.DNI,mesa=c.mesa,codigoPostal=c.codigoPostal,ciudad=c.ciudad,circunscripcion=c.circunscripcion)
		c.delete()
		ciudadano.save()
		return redirect('Partido:detallesPartido', partido.id)
	else:
		context = {'ciudadano':c}
		return render(request,'Ciudadano/borrarCiudadano.html',context)

#Funcion para editar un ciudadano/candidato
@login_required(login_url='Ciudadano:entrar')
def editarCiudadano(request,ciudadano_id):
	if request.method == 'POST':
		if Candidato.objects.filter(id=ciudadano_id).count():
			candidato=Candidato.objects.get(id=ciudadano_id)
			form = editarCandidatoForm(request.POST, instance=candidato)
		else:
			ciudadano=Ciudadano.objects.get(id=ciudadano_id)
			form = editarCiudadanoForm(request.POST, instance=ciudadano)
			
		if form.is_valid():
			form.save()
			if Candidato.objects.filter(id=ciudadano_id).count():
				return redirect('Ciudadano:detallesCandidato', ciudadano_id)
			else:
				return redirect('Ciudadano:detallesCiudadano', ciudadano_id)		
	else:
		if Candidato.objects.filter(id=ciudadano_id).count():
			candidato=Candidato.objects.get(id=ciudadano_id)
			if candidato.username == request.user.username or request.user.is_staff: #Comprobamos que sea el candidato en cuestion para modificar sus datos o que sea administrador
				form = editarCandidatoForm(instance=candidato)
			else:
				mensaje="No puedes editar otros candidatos"
				context={'mensaje':mensaje,'candidato':candidato}
				return render(request,'Ciudadano/detallesCandidato.html',context)	
		else:
			ciudadano=Ciudadano.objects.get(id=ciudadano_id)
			if ciudadano.username == request.user.username or request.user.is_staff: #Comprobamos que sea el ciudadano en cuestion para modificar sus datos o que sea administrador
				form = editarCiudadanoForm(instance=ciudadano)
			else:
				mensaje="No puedes editar otros ciudadanos"
				context={'mensaje':mensaje,'ciudadano':ciudadano}
				return render(request,'Ciudadano/detallesCiudadano.html',context)	
		context = {'form':form}
		return render(request,'Ciudadano/editarCiudadano.html',context)		
	
#Funcion para ver todos los ciudadanos
@staff_member_required
def verCiudadanos(request):
	mensaje = None
	ciudadanos = Ciudadano.objects.all()
	query = request.GET.get('q')
	if query:
		ciudadanos = ciudadanos.filter(
			Q(DNI__icontains=query) |
			Q(codigoPostal__icontains=query) |
			Q(first_name__icontains=query) |
			Q(last_name__icontains=query)
			).distinct()
		if not ciudadanos.count(): #Si no hay ciudadanos con esa caracteristica mostramos todos
			mensaje = "No hay ciudadanos con esa caracteristica" 
			ciudadanos = Ciudadano.objects.all()
	else:
		if not ciudadanos.count():
			mensaje = "No hay ciudadanos en la base de datos"
	context = {'ciudadanos':ciudadanos,'mensaje':mensaje}
	return render(request,'Ciudadano/verCiudadanos.html',context)

#Funcion para iniciar sesion
def entrar(request):
	mensaje = None
	if request.user.is_authenticated():
		mensaje = "Ya se encuentra logueado en el sistema"
		context = {'mensaje':mensaje}
		return render(request,'djangoPW/index.html',context)
	else:
		if request.method == 'POST':
			form = loginForm(request.POST)
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request,user)
				mensaje = "Se ha logueado correctamente en el sistema"
				context = {'mensaje':mensaje}
				return render(request,'djangoPW/index.html',context)
			else:
				mensaje = "No se ha logueado correctamente en el sistema. Compruebe que su nombre de usuario y password son correctos"
				context = {'mensaje':mensaje,'form':form}
				return render(request,'Ciudadano/login.html',context)
		else:
			form = loginForm()
		context = {'form':form}
		return render(request,'Ciudadano/login.html',context)
		


#Funcion para cerrar sesion
@login_required(login_url='Ciudadano:entrar')
def salir(request):
	if request.method == 'POST':
		logout(request)
		return redirect('index')
	else:
		return render(request,'Ciudadano/logout.html')
		
#Funcion para cambiar la contrasenia
@login_required(login_url='Ciudadano:entrar')
def cambiarContrasenia(request):
	ciudadano=get_object_or_404(Ciudadano, username=request.user.get_username())
	mensaje = None
	if request.method == 'POST':
		password_actual= request.POST['password_actual']
		password = request.POST['password']
		password_check = request.POST['password_check']

		if ciudadano.check_password(password_actual):
			if password == password_check:
				ciudadano.set_password(password)
				ciudadano.save()
				# Cuando cambiamos la contrasenia del ciudadano se cierra la sesion, por lo que le hacemos un login automatico
				user = authenticate(username=ciudadano.username, ciudadano=password)
				if user is not None:
					login(request, user)
					return redirect('Ciudadano:detallesCiudadano',ciudadano.id)
				else:
					return redirect('Ciudadano:entrar')
				
			else:
				mensaje = "Las contrasenias no coinciden"
				form = CambiarContraseniaForm()
		else:
			mensaje = "Esa no es su contrasenia actual"
			form = CambiarContraseniaForm()
	else:
		form = CambiarContraseniaForm()
	context={'mensaje':mensaje,'form':form}
	return render(request, 'Ciudadano/cambiarContrasenia.html',context)

	
