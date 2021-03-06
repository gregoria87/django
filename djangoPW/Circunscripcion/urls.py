from django.conf.urls import url
from . import views, forms
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required

app_name='Circunscripcion'
urlpatterns = [
	
	url(r'^votar/$',views.votar,name='votar'),
	url(r'^resultados/$',views.verResultados,name='verResultados'),
	url(r'^crearCircunscripcion/$',views.crearCircunscripcion,name='crearCircunscripcion'),
	url(r'^mostrarCircunscripciones/$',views.verCircunscripciones.as_view(),name='mostrarCircunscripciones'),
	url(r'^verCircunscripcionDetalle/(?P<circunscripcion_id>[0-9]+)/$',views.verCircunscripcionDetalle,name='verCircunscripcionDetalle'),
	url(r'^modificarCircunscripcion/(?P<pk>[0-9]+)/$',staff_member_required(views.modificarCircunscripcion.as_view()),name='modificarCircunscripcion'),
	url(r'^(?P<pk>[0-9]+)/borrarCircunscripcion/$',staff_member_required(views.borrarCircunscripcion.as_view()),name='borrarCircunscripcion'),

] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
