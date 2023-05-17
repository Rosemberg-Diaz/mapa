from asyncio.windows_events import NULL
import googlemaps
import gmaps
from datetime import datetime
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core import serializers
import requests
import json
import urllib

import base64
from django.contrib.auth import logout, login as auth_login
from google.backends import CustomAuthBackend
from .decorators import user_login_required
from bson.objectid import ObjectId

''' Esta vista maneja la solicitud de registro de un nuevo usuario. Si la petición es una solicitud POST,
 se recogen los datos del formulario y se crea un nuevo usuario con la función create_user del modelo Usuarios.'''

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['clave']
        email = request.POST['email']
        Usuarios.objects.create_user(email, username, contraseña)
        return redirect('inicio')
    else:
        return render(request, 'Autenticacion/registro.html')

''' Esta vista maneja la solicitud de inicio de sesión de un usuario existente. Si la petición es una solicitud POST, 
se recogen los datos del formulario y se utiliza la función authenticate del backend personalizado CustomAuthBackend para autenticar al usuario.'''

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        contraseña = request.POST['contraseña']
        user = CustomAuthBackend().authenticate(
            request, email=email, contraseña=contraseña)
        if user is not None:
            request.session['user_id'] = str(user.pk)
            return redirect('map')
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos'
    else:
        error_message = None
    return render(request, 'Autenticacion/login.html', {'error_message': error_message})



'''Esta vista devuelve el objeto de usuario correspondiente a la sesión actual del usuario.'''

def get_user(request):
    user_id = request.session.get('user_id')
    user_id = ObjectId(user_id)
    return Usuarios.objects.get(pk=user_id)


def vistaBase(request):
    return render(request, "Autenticacion/base.html")


'''Esta vista maneja la solicitud de cierre de sesión de un usuario'''

@user_login_required
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # delete user session
    return redirect('inicio')



'''Esta vista renderiza la página de inicio después de que un usuario haya iniciado sesión.'''

@user_login_required
def home(request):
    context = {}
    return render(request, 'google/home.html', context)



'Esta vista renderiza la página de geocodificación de la aplicación y muestra una lista de empresas en la base de datos.'

@user_login_required
def geocode(request):
    empresa = Empresas.objects.all()
    context = {
        'empresas': empresa,
    }
    return render(request, 'google/geocode.html', context)



'''Este metodo se utiliza para crear una nueva empresa. En primer lugar, se obtienen todas las ciudades disponibles de la base de datos. Luego, 
si la solicitud del usuario es un método POST, se valida la información ingresada por el usuario utilizando un formulario. 
Si el formulario es válido, se crea una nueva entrada en la tabla de Empresas de la base de datos y se guarda. '''

@user_login_required
def crearEmpresa(request):
    ciudades = Ciudades.objects.all()
    if request.method == 'POST':
        details = empresaForm(request.POST)
        if details.is_valid():
            nit = request.POST['NIT']
            if len(nit) != 9 or not nit.isdigit():
                details.add_error('NIT', 'El NIT debe ser un número de 9 dígitos')
                return render(request, "Empresas/create.html", {'form': details, 'ciudades': ciudades})
            # if Empresas.objects.filter(NIT=nit).exists():
            #      details.add_error('NIT', 'Ya existe una empresa con este NIT')
            #      return render(request, "Empresas/create.html", {'form': details, 'ciudades': ciudades})

            post = details.save(commit=False)
            post.save()
            p = Empresas.objects.get(NIT=request.POST['NIT'])
            ciudad = Ciudades.objects.get(nombre=request.POST['ciudad'])
            p.estado = True
            p.ciudad = ciudad
            p.fechaFundacion = request.POST['fechaFundacion']
            p.save()
            return redirect('geocode_club', request.POST['NIT'])
        else:
            return render(request, "Empresas/create.html", {'form': details, 'ciudades': ciudades})
    else:
        form = empresaForm(None)
        return render(request, 'Empresas/create.html', {'form': form, 'ciudades': ciudades})



'''se utiliza para crear una nueva sede de una empresa. Al igual que en la función anterior,
 se obtienen todas las ciudades disponibles de la base de datos y todas las empresas existentes.
 Si la solicitud del usuario es un método POST, se valida la información ingresada por el usuario utilizando un formulario. '''
#
# @user_login_required
# def crearSede(request):
#     ciudades = Ciudades.objects.all()
#     empresas = Empresas.objects.all()
#     if request.method == 'POST':
#         details = sedeForm(request.POST)
#         if details.is_valid():
#             nombre = request.POST['nombre']
#             post = details.save(commit=False)
#             post.save()
#             p = Sedes.objects.get(nombre=nombre)
#             ciudad = Ciudades.objects.get(nombre=request.POST['ciudad'])
#             empresa = Empresas.objects.get(nombre=request.POST['empresa'])
#             p.ciudad = ciudad
#             p.empresa = empresa
#             p.save()
#             return redirect('geocode_club', request.POST['nombre'])
#         else:
#             return render(request, "Sedes/create.html", {'form': details, 'ciudades': ciudades, 'empresas': empresas})
#     else:
#         form = sedeForm(None)
#         return render(request, 'Sedes/create.html', {'form': form, 'ciudades': ciudades, 'empresas': empresas})



''' se utiliza para editar la información de una empresa existente. Se obtiene el objeto Empresa correspondiente a la NIT proporcionada.
 Si la solicitud del usuario es un método POST, se valida la información ingresada por el usuario utilizando un formulario. Si el formulario es válido, 
se actualiza la entrada en la tabla de Empresas de la base de datos y se guarda'''

@user_login_required
def editarEmpresa(request, NIT):
    empresa = get_object_or_404(Empresas, NIT=NIT)
    ciudades = Ciudades.objects.all()

    if request.method == 'POST':
        form = empresaForm(request.POST, instance=empresa)
        if form.is_valid():
            nit = request.POST['NIT']
            valor = int(nit)
            if len(nit) != 9 or not nit.isdigit():
                form.add_error('NIT', 'El NIT debe ser un número de 9 dígitos')
                return render(request, "Empresas/edit.html", {'form': form, 'ciudades': ciudades, 'nit': valor, 'empresa':empresa})

            post = form.save(commit=False)
            ciudad = Ciudades.objects.get(nombre=request.POST['ciudad'])
            fechaFundacion = request.POST['fechaFundacion']
            post.ciudad = ciudad
            post.fechaFundacion = fechaFundacion
            post.save()
            return redirect('geocode_club', empresa.NIT)
        else:
            return render(request, "Empresas/edit.html", {'form': form, 'ciudades': ciudades, 'nit': NIT, 'empresa':empresa})
    else:
        form = empresaForm(instance=empresa)
        return render(request, 'Empresas/edit.html', {'form': form, 'ciudades': ciudades, 'nit': NIT, 'empresa':empresa})




'''Función que se encarga de cambiar el estado de una empresa a inactivo. Recibe una solicitud HTTP (request) y un número de identificación tributaria (NIT) como parámetros.
 Primero se busca la empresa correspondiente a NIT utilizando la función get_object_or_404 de Django. 
Luego, se cambia el valor del estado de la empresa a False y se guarda en la base de datos. '''

def inactivarEmpresa(request, NIT):
    empresa = get_object_or_404(Empresas, NIT=NIT)
    empresa.estado = False
    empresa.save()
    return redirect('geocode_club', empresa.NIT)




''' Función que se encarga de obtener la latitud y longitud de una dirección de una empresa y guardarla en la base de datos. 
Recibe una solicitud HTTP (request) y un número de identificación tributaria (pk) como parámetros.
 Primero, se busca la empresa correspondiente a pk utilizando la función get de Django. Luego, se verifica si la dirección de la empresa ya se encuentra en la base de datos.
   Si es así, se crea una cadena de texto que contiene la dirección, la ciudad y el país donde se encuentra la empresa. Luego,
 se utiliza la API de Google Maps para obtener la latitud y longitud correspondiente a la dirección y se guarda en la base de datos. '''

def geocode_club(request, pk):
    empresa = Empresas.objects.get(NIT=pk)
    # check whether we have the data in the database that we need to calculate the geocode
    if empresa.direccion:
        # creating string of existing location data in database
        adress_string = str(empresa.direccion) + ', ' + str(empresa.ciudad) + ", Valle del Cauca, Colombia"

        # geocode the string
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        intermediate = json.dumps(gmaps.geocode(str(adress_string)))
        intermediate2 = json.loads(intermediate)
        latitude = intermediate2[0]['geometry']['location']['lat']
        longitude = intermediate2[0]['geometry']['location']['lng']
        # save the lat and long in our database
        empresa.latitude = latitude
        empresa.longitude = longitude
        empresa.save()
        return redirect('map')
    else:
        return redirect('map')
    return render(request, 'google/empty.html', context)



'''Función que se encarga de renderizar la página map.html con los datos necesarios. 
Recibe una solicitud HTTP (request) como parámetro. Primero, se obtiene el usuario que ha realizado la solicitud utilizando la función get_user de Django. 
Luego, se crea un diccionario que contiene la clave key con el valor de la clave de la API de Google Maps y la clave user con el objeto user anteriormente obtenido. '''

@user_login_required
def mapa(request):
    user = get_user(request)
    print(user.pk)
    key = settings.GOOGLE_API_KEY
    empres =  Empresas.objects.all()
    empresBusqueda= []
    nombres= []
    for i in empres:
        print(empres)
        nombres.append(i.nombre)
    print(nombres)
    if request.method == 'POST':
        for nombre in nombres:
            if request.POST['search'] in nombre:
                emp = Empresas.objects.get(nombre=nombre)
                empresBusqueda.append(emp)
        if(len(empresBusqueda)==0):
            context = {
                'key': key,
                'user': user,
                'Empresa': empres,
                'lati': 3.43722,
                'longi': -76.5225,
                'zoom': 12
            }
        else:
            context = {
                'key': key,
                'user': user,
                'lati': emp.latitude,
                'longi': emp.longitude,
                'Empresa': empresBusqueda,
                'zoom': 15
            }
    else:
        context = {
            'key': key,
            'user': user,
            'lati': 3.43722,
            'longi': -76.5225,
            'zoom': 12
        }
    return render(request, 'google/map.html', context)


''' Función que se encarga de obtener los datos de todas las empresas y empleados, devolverlos en formato JSON.
 Recibe una solicitud HTTP (request) como parámetro. Primero, se obtienen los datos de todas las empresas y se almacenan en una lista.
 Luego, se devuelve la lista en formato JSON utilizando la función JsonResponse de Django.'''

def mydata(request):
    result_list = list(Empresas.objects.values('nombre',
                                               'descripcion',
                                               'NIT',
                                               'mision',
                                               'vision',
                                               'telefono',
                                               'fechaFundacion',
                                               'paginaWeb',
                                               'direccion',
                                               'latitude',
                                               'longitude',
                                               ))

    return JsonResponse(result_list, safe=False)



''' Función que se encarga de renderizar la página listaEmp.html con la lista de empleados de una empresa.
 Recibe una solicitud HTTP (request) y el nombre de la empresa (rest) como parámetros.
 Primero, se busca la empresa correspondiente al nombre utilizando la función get de Django. 
Luego, se obtienen los empleados de la empresa utilizando la función filter de Django. '''

@user_login_required
def vistaListaEmpl(request, rest):
    emp = Empresas.objects.get(nombre=rest)
    empleados = Empleados.objects.filter(empresa=emp)
    user = get_user(request)
    nombres = []
    completo = []
    busqueda = []
    for i in empleados:
        nombre = i.nombres+ " "+ i.apellidos
        nombres.append(nombre)
        completo.append(i)
    if request.method == 'POST':
        for idx in range(len(nombres)):
            if request.POST['search'] in nombres[idx]:
                busqueda.apennd(empleados[idx])
    else:
        context = {
            'emp': rest,
            'empleados': empleados,
            'user': user,
        }
    if len(busqueda)==0:
        context = {
            'emp': rest,
            'empleados': empleados,
            'user': user,
        }
    else:
        context = {
            'emp': rest,
            'empleados': busqueda,
            'user': user,
        }
    return render(request, "google/listaEmp.html", context=context)


'''esta función toma un archivo como entrada, lo lee y lo codifica en Base64. Luego devuelve la cadena codificada en Base64.'''
def encode_file(file):
    # Lee los datos del archivo
    data = file.read()
    # Codifica los datos en Base64
    encoded_data = base64.b64encode(data)
    encoded_string = encoded_data.decode('utf-8')
    return (encoded_string)


'''esta función maneja la creación de nuevos empleados en la base de datos. Si se envía un formulario válido (a través de una solicitud POST),
 crea un objeto Empleados a partir de los datos del formulario y lo guarda en la base de datos.'''
@user_login_required
def vistaCrearEmpl(request, rest):
    if request.method == 'POST':

        # Pass the form data to the form class
        details = empleadoForm(request.POST, request.FILES)
        # In the 'form' class the clean function
        # is defined, if all the data is correct
        # as per the clean function, it returns true
        if details.is_valid():
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)
            imagen = encode_file(request.FILES['uploadFromPC'])
            # Finally write the changes into database
            post.save()
            p = Empleados.objects.get(documento=request.POST['documento'])
            emp = Empresas.objects.get(nombre=rest)
            p.imagen = imagen
            p.empresa = emp
            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect('map')

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "Empleados/crearEmp.html", {'form': details})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = empleadoForm(None)
        return render(request, 'Empleados/crearEmp.html', {'form': form})


'''
esta función maneja la edición de los detalles de un empleado existente. Si se envía un formulario válido (a través de una solicitud POST),
actualiza los campos correspondientes del objeto Empleados y lo guarda en la base de datos.
'''

@user_login_required
def vistaEditarEmpl(request, rest, ced):
    p = Empleados.objects.get(documento=ced)
    print(p)
    if request.method == "POST":
        print("Entro 1")
        form = empleadoForm(request.POST, request.FILES, instance=p)
        print(request.POST['nombres'])
        if form.is_valid():
            p.nombres = request.POST['nombres']
            p.apellidos = request.POST['apellidos']
            p.experiencia = request.POST['experiencia']
            p.telefono = request.POST['telefono']
            p.email = request.POST['email']
            p.documento = request.POST['documento']
            p.cargo = request.POST['cargo']
            p.experiencia = request.POST['experiencia']
            p.experienciaCargo = request.POST['experienciaCargo']
            print("Entro")
            if (request.POST['uploadFromPC'] != ''):
                imagen = encode_file(request.FILES['uploadFromPC'])
                p.imagen = imagen
            if (request.POST['video'] != ''):
                entrevista = encode_file(request.FILES['video'])
                permisos = encode_file(request.FILES['pdf'])
                p.entrevista = entrevista
                p.permiso = permisos
            print("Entro")
            print(p)
            p.save()
            return redirect('map')
        else:
            form = empleadoForm(instance=p)
            return render(request, 'Empleados/editarEmp.html', {'form': form, 'emp':p})
    else:
        form = empleadoForm(instance=p)
        return render(request, "Empleados/editarEmp.html", {'form': form, 'emp':p})


'''esta función muestra los detalles de un empleado existente en una página separada.'''
@user_login_required
def vistaVerEmpl(request, rest, ced):
    empleados = Empleados.objects.get(documento=ced)
    context = {
        'emp': rest,
        'empleado': empleados,
    }
    return render(request, "Empleados/verPersonal.html", context=context)

@user_login_required
def estadoEmp(request, rest, ced):
    empleados = Empleados.objects.get(documento=ced)
    context = {
        'emp': rest,
        'empleado': empleados,
    }
    if(empleados.estado == 'Activo'):
        empleados.estado = 'Inactivo'
    else:
        empleados.estado = 'Activo'
    empleados.save()
    return redirect('map')