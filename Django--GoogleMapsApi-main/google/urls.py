from .views import *
from django.urls import path, include
from google import views as view

urlpatterns = [
   path('home',view.home, name="home"),
   path('geocode',view.geocode, name="geocode"),
   path('geocode/club/<int:pk>',view.geocode_club, name="geocode_club"),
   path('',view.map, name="map"),
   path('mydata',view.mydata, name="mydata"),
   path('crearEmpresa', view.crearEmpresa, name='crearEmpresa'),
   path('listaEmp/', view.vistaListaEmpl, name='listaEmp'),
   path('crearEmp/', view.vistaCrearEmpl, name='crearEmp'),
   path('editarEmp/', view.vistaEditarEmpl, name='editarEmp'),
   path('verEmp/', view.vistaVerEmpl, name='verEmp'),
]