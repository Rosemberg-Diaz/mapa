from .views import *
from django.urls import path, include
from googleApp import views as view

urlpatterns = [
    path('', view.vistaBase, name='inicio'),
    path('registro/', view.registro, name='registro'),
    path('login/', view.login, name='login'),
    path('logout/', view.logout_view, name='logout'),
    path('home', view.home, name="home"),
    path('geocode', view.geocode, name="geocode"),
    path('geocode/club/<int:pk>', view.geocode_club, name="geocode_club"),
    path('geocode_sede/club/<str:pk>', view.geocode_club_sede, name="geocode_club_sede"),
    path('mapa/', view.mapa, name="map"),
    path('mapa_sede/', view.mapa_sede, name="map_sede"),
    path('mydata', view.mydata, name="mydata"),
    path('mydataSede', view.mydataSede, name="mydataSede"),
    path('crearEmpresa', view.crearEmpresa, name='crearEmpresa'),
    path('editarEmpresa/<NIT>', view.editarEmpresa, name='editarEmpresa'),
    path('inactivarEmpresa/<NIT>', view.inactivarEmpresa, name='inactivarEmpresa'),
    path('crearSede/<str:rest>', view.crearSede, name='crearSede'),
    path('editarSede/<nombre>', view.editarSede, name='editarSede'),
    path('inactivarSede/<nombre>', view.inactivarSede, name='inactivarSede'),
    path('listaEmp/<str:rest>/', view.vistaListaEmpl, name='listaEmp'),
    path('crearEmp/<str:rest>/', view.vistaCrearEmpl, name='crearEmp'),
    path('editarEmp/<str:rest>/<str:ced>/', view.vistaEditarEmpl, name='editarEmp'),
    path('verEmp/<str:rest>/<str:ced>/', view.vistaVerEmpl, name='verEmp'),
    path('estadoEmp/<str:rest>/<str:ced>/', view.estadoEmp, name='estadoEmp'),
    path('mydataBusqueda', view.mydataBusqueda, name="mydataBusqueda"),
]
