from .views import *
from django.urls import path, include
from googleApp import views as view
'La página define las rutas y direcciones URL del proyecto. Cada ruta especifica una URL y la función de vista asociada que se ejecutará cuando se acceda a esa URL en el navegador.'
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
   path('obtener_Ser_Esp/',view.obtener_Ser_Esp, name="obtener_Ser_Esp"),
   path('crearEmpresa', view.crearEmpresa, name='crearEmpresa'),
   path('editarEmpresa/<NIT>', view.editarEmpresa, name='editarEmpresa'),
   path('inactivarEmpresa/<NIT>', view.inactivarEmpresa, name='inactivarEmpresa'),
  # path('crearSede', view.crearSede, name='crearSede'),
   path('listaEmp/<str:rest>/', view.vistaListaEmpl, name='listaEmp'),
   path('crearEmp/<str:rest>/', view.vistaCrearEmpl, name='crearEmp'),
   path('editarEmp/<str:rest>/<str:ced>/', view.vistaEditarEmpl, name='editarEmp'),
   path('verEmp/<str:rest>/<str:ced>/', view.vistaVerEmpl, name='verEmp'),
   path('estadoEmp/<str:rest>/<str:ced>/', view.estadoEmp, name='estadoEmp'),
   path('mydataBusqueda',view.mydataBusqueda, name="mydataBusqueda"),
]