from django.conf.urls import url
from . import views, forms
from django.conf import settings
from django.conf.urls.static import static

app_name='Partido'
urlpatterns = [
	url(r'^mostrarPartidos/$',views.mostrarPartidos.as_view(),name='mostrarPartidos'),
	url(r'^detallesPartido/(?P<partido_id>\d+)/$',views.detallesPartido, name='detallesPartido'),
	url(r'^(?P<partido_id>\d+)/agregarCircunscripcion/$',views.agregarPartidoCircunscripcion,name='agregarPartidoCircunscripcion'),
	url(r'^crearPartido/$',views.crearPartido, name='crearPartido'),
	url(r'^modificarPartido/(?P<partido_id>\d+)/$',views.modificarPartido, name='modificarPartido'),
	url(r'^borrarPartido/(?P<partido_id>[0-9]+)/$',views.borrarPartido, name='borrarPartido')
	

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
