from .views import *
from django.urls import path, include
from googleApp import views as view

urlpatterns = [
   path('', view.vistaBase, name='inicio'),
   path('registro/', view.registro, name='registro'),
   path('login/', view.login, name='login'),
   path('logout/', view.logout_view, name='logout'),
   path('home',view.home, name="home"),
   path('geocode',view.geocode, name="geocode"),
   path('geocode/club/<int:pk>',view.geocode_club, name="geocode_club"),
   path('mapa/',view.mapa, name="map"),
   path('mydata',view.mydata, name="mydata"),
   path('crearEmpresa', view.crearEmpresa, name='crearEmpresa'),
   path('editarEmpresa/<NIT>', view.editarEmpresa, name='editarEmpresa'),
   path('inactivarEmpresa/<NIT>', view.inactivarEmpresa, name='inactivarEmpresa'),
  # path('crearSede', view.crearSede, name='crearSede'),
   path('listaEmp/<str:rest>/', view.vistaListaEmpl, name='listaEmp'),
   path('crearEmp/<str:rest>/', view.vistaCrearEmpl, name='crearEmp'),
   path('editarEmp/<str:rest>/<str:ced>/', view.vistaEditarEmpl, name='editarEmp'),
   path('verEmp/<str:rest>/<str:ced>/', view.vistaVerEmpl, name='verEmp'),
   path('estadoEmp/<str:rest>/<str:ced>/', view.estadoEmp, name='estadoEmp'),
]