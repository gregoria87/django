from django.conf.urls import url
from . import views, forms
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required

app_name='Ciudadano'
urlpatterns = [

	url(r'^detallesCandidato/(?P<pk>[0-9]+)/$',views.detallesCandidato.as_view(),name='detallesCandidato'),
	url(r'^detallesCiudadano/(?P<pk>[0-9]+)/$',views.detallesCiudadano.as_view(),name='detallesCiudadano'),
	url(r'^addCandidatoPartido/(?P<partido_id>[0-9]+)/$',views.addCandidato,name='addCandidatoPartido'),
	url(r'^crearCandidato/$',views.crearCandidato,name='crearCandidato'),
	url(r'^crearCiudadano/$',views.crearCiudadano,name='crearCiudadano'),
	url(r'^editarCiudadano/(?P<ciudadano_id>[0-9]+)/$',views.editarCiudadano,name='editarCiudadano'),
	url(r'^(?P<pk>[0-9]+)/borrarCiudadano/$',login_required(views.borrarCiudadano.as_view()),name='borrarCiudadano'),
	url(r'^(?P<candidato_id>[0-9]+)/borrarCandidato/$',views.borrarCandidato,name='borrarCandidato'),
	url(r'^addCandidato/(?P<partido_id>[0-9]+)/$',views.addCiudadanoComoCandidato,name='addCiudadanoComoCandidato'),
	url(r'^verCiudadanos/$',views.verCiudadanos,name='verCiudadanos'),
	url(r'^login/$',views.entrar,name='entrar'),
	url(r'^logout/$',views.salir,name='salir'),
	url(r'^modificarContrasenia$',views.cambiarContrasenia, name="modificarContrasenia"),
	
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
