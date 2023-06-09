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
from django.contrib import messages


import requests
import json
import urllib

import base64
from django.contrib.auth import logout, login as auth_login
from googleApp.backends import CustomAuthBackend
from .decorators import user_login_required

from bson import ObjectId
#Importaciones para cloud storage
from django.conf import settings
import os
from urllib.parse import urlparse
import mimetypes

#cloudinary
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from cloudinary import uploader
from cloudinary import CloudinaryResource
import cloudinary.utils

from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

mydataJ = []


''' Esta vista maneja la solicitud de registro de un nuevo usuario. Si la petición es una solicitud POST,
 se recogen los datos del formulario y se crea un nuevo usuario con la función create_user del modelo Usuarios.'''

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['clave']
        email = request.POST['email']
        Usuarios.objects.create_user(email, username, contraseña)
        messages.success(request, "EXITOSAMENTE CREADO")
        return redirect('inicio')
    else:
        messages.error(request, "ERROR EN LA CREACIÓN")
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
            messages.success(request, "INGRESADO EXITOSAMENTE")
            return redirect('map')
        else:
            error_message = 'Nombre de usuario o contraseña incorrectos'
    else:
        error_message = None
        messages.error(request, "ERROR EN EL INGRESO")
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
    servicios = Servicios.objects.all()
    especialidades = Especialidades.objects.all()
    if request.method == 'POST':
        details = empresaForm(request.POST)
        print("antes de")
        print(details.is_valid())
        print("no sé")
        if details.is_valid():
            nit = request.POST['NIT']
            especialidades_ids = request.POST.getlist('especialidades')
            especialidades = [ObjectId(especialidad_id) for especialidad_id in especialidades_ids]
            servicios_ids = request.POST.getlist('servicios')
            servicios = [ObjectId(especialidad_id) for especialidad_id in servicios_ids]
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
            p.servicios.set(servicios)
            p.especialidades.set(especialidades)
            p.save()
            messages.success(request, "EMPRESA EXITOSAMENTE CREADA")
            return redirect('geocode_club', request.POST['NIT'])
        else:
            messages.error(request, "ERROR EN LA CREACIÓN")
            return render(request, "Empresas/create.html", {'form': details, 'ciudades': ciudades,
                                                            "especialidades":especialidades, "servicios":servicios})
    else:
        form = empresaForm(None)
        return render(request, 'Empresas/create.html', {'form': form, 'ciudades': ciudades,
                                                        "especialidades":especialidades, "servicios":servicios})



'''se utiliza para crear una nueva sede de una empresa. Al igual que en la función anterior,
 se obtienen todas las ciudades disponibles de la base de datos y todas las empresas existentes.
 Si la solicitud del usuario es un método POST, se valida la información ingresada por el usuario utilizando un formulario. '''

@user_login_required
def crearSede(request, rest):
    ciudades = Ciudades.objects.all()
    empresas = Empresas.objects.all()
    if request.method == 'POST':
        details = sedeForm(request.POST)
        if details.is_valid():
            nombre = request.POST['nombre']
            post = details.save(commit=False)
            post.save()
            s = Sedes.objects.get(nombre=nombre)
            ciudad = Ciudades.objects.get(nombre=request.POST['ciudad'])
            empresa = Empresas.objects.get(nombre=rest)
            s.ciudad = ciudad
            s.empresa = empresa
            s.save()
            messages.success(request, "SEDE EXITOSAMENTE CREADA")
            return redirect('geocode_club_sede', request.POST['nombre'])
        else:
            messages.error(request, "ERROR EN LA CREACIÓN")
            return render(request, "Sedes/create.html", {'form': details, 'ciudades': ciudades, 'empresas': empresas})
    else:
        form = sedeForm(None)
        return render(request, 'Sedes/create.html', {'form': form, 'ciudades': ciudades, 'empresas': empresas})



''' se utiliza para editar la información de una empresa existente. Se obtiene el objeto Empresa correspondiente a la NIT proporcionada.
 Si la solicitud del usuario es un método POST, se valida la información ingresada por el usuario utilizando un formulario. Si el formulario es válido, 
se actualiza la entrada en la tabla de Empresas de la base de datos y se guarda'''

@user_login_required
def editarEmpresa(request, NIT):
    empresa = get_object_or_404(Empresas, NIT=NIT)
    ciudades = Ciudades.objects.all()
    servicios = Servicios.objects.all()
    especialidades = Especialidades.objects.all()

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

            especialidades_ids = request.POST.getlist('especialidades')
            servicios_ids = request.POST.getlist('servicios')

            especialidades = [ObjectId(especialidad_id) for especialidad_id in especialidades_ids]
            servicios = [ObjectId(especialidad_id) for especialidad_id in servicios_ids]

            post.especialidades.clear()
            post.servicios.clear()

            post.especialidades.set(especialidades)
            post.servicios.set(servicios)

            messages.success(request, "EXITOSAMENTE ACTUALIZADO")
            return redirect('geocode_club', empresa.NIT)
        else:
            messages.error(request, "ERROR EN LA ACTUALIZACIÓN DE DATOS")
            return render(request, "Empresas/edit.html", {'form': form, 'ciudades': ciudades, 'nit': NIT, 'empresa':empresa, 'especialidades': especialidades, 'servicios': servicios})
    else:
        form = empresaForm(instance=empresa)
        return render(request, 'Empresas/edit.html', {'form': form, 'ciudades': ciudades, 'nit': NIT, 'empresa':empresa, 'especialidades': especialidades, 'servicios': servicios})



@user_login_required
def editarSede(request, nombre):
    sede = get_object_or_404(Sedes, nombre=nombre)
    ciudades = Ciudades.objects.all()
    empresas = Empresas.objects.all()

    if request.method == 'POST':
        form = sedeForm(request.POST, instance=sede)
        if form.is_valid():
            post = form.save(commit=False)
            ciudad = Ciudades.objects.get(nombre=request.POST['ciudad'])
            # empresa = Empresas.objects.get(nombre=request.POST['empresa'])
            post.ciudad = ciudad
            # post.empresa = empresa
            post.save()
            messages.success(request, "Sede actualizada exitosamente")
            return redirect('geocode_club_sede', sede.nombre)
        else:
            messages.error(request, "Error al actualizar la sede")
            return render(request, 'Sedes/edit.html',
                          {'form': form, 'ciudades': ciudades, 'nombre': nombre, 'empresas': empresas})
    else:
        form = sedeForm(instance=sede)
    return render(request, 'Sedes/edit.html',
                  {'form': form, 'ciudades': ciudades, 'nombre': nombre, 'empresas': empresas})

'''Función que se encarga de cambiar el estado de una empresa a inactivo. Recibe una solicitud HTTP (request) y un número de identificación tributaria (NIT) como parámetros.
 Primero se busca la empresa correspondiente a NIT utilizando la función get_object_or_404 de Django. 
Luego, se cambia el valor del estado de la empresa a False y se guarda en la base de datos. '''

def inactivarEmpresa(request, NIT):
    empresa = get_object_or_404(Empresas, NIT=NIT)
    empresa.estado = False
    empresa.save()
    messages.success(request, "LA EMPRESA SE INACTIVO CORRECTAMENTE")
    return redirect('geocode_club', empresa.NIT)



def inactivarSede(request, nombre):
    sede = get_object_or_404(Sedes, nombre=nombre)
    sede.estado = False
    sede.save()
    messages.success(request, "LA SEDE SE INACTIVO CORRECTAMENTE")
    return redirect('geocode_club_sede', sede.nombre)


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



def geocode_club_sede(request, pk):
    sede = Sedes.objects.get(nombre=pk)
    # check whether we have the data in the database that we need to calculate the geocode
    if sede.direccion:
        # creating string of existing location data in database
        adress_string = str(sede.direccion) + ', ' + str(sede.ciudad) + ", Valle del Cauca, Colombia"

        # geocode the string
        gmaps = googlemaps.Client(key=settings.GOOGLE_API_KEY)
        intermediate = json.dumps(gmaps.geocode(str(adress_string)))
        intermediate2 = json.loads(intermediate)
        latitude = intermediate2[0]['geometry']['location']['lat']
        longitude = intermediate2[0]['geometry']['location']['lng']
        # save the lat and long in our database
        sede.latitude = latitude
        sede.longitude = longitude
        sede.save()
        return redirect('map_sede')
    else:
        return redirect('map_sede')
    return render(request, 'google/empty.html', context)

'''Función que se encarga de renderizar la página map.html con los datos necesarios. 
Recibe una solicitud HTTP (request) como parámetro. Primero, se obtiene el usuario que ha realizado la solicitud utilizando la función get_user de Django. 
Luego, se crea un diccionario que contiene la clave key con el valor de la clave de la API de Google Maps y la clave user con el objeto user anteriormente obtenido. '''

@user_login_required
def mapa(request):
    user = get_user(request)
    key = settings.GOOGLE_API_KEY
    empres = Empresas.objects.all()
    nombres= []
    for i in empres:
        nombres.append(i.nombre)
    if request.method == 'POST':
        for nombre in nombres:
            if request.POST['search'] in nombre:
                mydataJ.clear()
                emp = Empresas.objects.get(nombre=nombre)
                mydataJ.append({'nombre': emp.nombre,
                                'NIT': emp.NIT,
                                'mision': emp.mision,
                                'vision': emp.vision,
                                'descripcion': emp.descripcion,
                                'telefono': emp.telefono,
                                'paginaWeb': emp.paginaWeb,
                                'fechaFundacion': emp.fechaFundacion,
                                'direccion': emp.direccion,

                                'ciudad__nombre': emp.ciudad.nombre,
                                'servicios__nombre': [servicio.nombre for servicio in emp.servicios.all()],
                                'especialidades__nombre': [especialidad.nombre for especialidad in emp.especialidades.all()],

                         'latitude': emp.latitude,
                        'longitude': emp.longitude
                })
        if(len(mydataJ)==0):
            context = {
                'key': key,
                'user': user,
                'data': True,
                'lati': 3.43722,
                'longi': -76.5225,
                'zoom': 12
            }
        else:
            context = {
                'key': key,
                'user': user,
                'lati': 3.43722,
                'longi': -76.5225,
                'data': False,
                'zoom': 12
            }
    else:
        context = {
            'key': key,
            'user': user,
            'data': True,
            'lati': 3.43722,
            'longi': -76.5225,
            'zoom': 12
        }
    return render(request, 'google/map.html', context)


def mydataBusqueda(request):

    return JsonResponse(mydataJ, safe=False)



def mapa_sede(request):
    user = get_user(request)
    key = settings.GOOGLE_API_KEY
    sede = Sedes.objects.all()
    nombres = []
    for i in sede:
        nombres.append(i.nombre)
    if request.method == 'POST':
        for nombre in nombres:
            if request.POST['search'] in nombre:
                sed = Sedes.objects.get(nombre=nombre)
                mydataJ.append({'nombre': sed.nombre,
                                'latitude': sed.latitude,
                                'longitude': sed.longitude
                                })
        if (len(mydataJ) == 0):
            context = {
                'key': key,
                'user': user,
                'data': True,
                'lati': 3.43722,
                'longi': -76.5225,
                'zoom': 12
            }
        else:
            context = {
                'key': key,
                'user': user,
                'lati': 3.43722,
                'longi': -76.5225,
                'data': False,
                'zoom': 12
            }
    else:
        context = {
            'key': key,
            'user': user,
            'data': True,
            'lati': 3.43722,
            'longi': -76.5225,
            'zoom': 12
        }
    return render(request, 'google/map.html', context)



''' Función que se encarga de obtener los datos de todas las empresas y empleados, devolverlos en formato JSON.
 Recibe una solicitud HTTP (request) como parámetro. Primero, se obtienen los datos de todas las empresas y se almacenan en una lista.
 Luego, se devuelve la lista en formato JSON utilizando la función JsonResponse de Django.'''

def mydata(request):

    result_list = list(Empresas.objects.values('nombre', 'descripcion', 'NIT', 'mision', 'vision', 'telefono',
                                               'fechaFundacion', 'paginaWeb', 'direccion', 'latitude', 'longitude',
                                               'estado','especialidades__nombre',
                                               # Accede al campo 'nombre' de la relación especialidades
                                               'servicios__nombre',
                                               'ciudad__nombre'))

    result_list2 = list(Sedes.objects.values('nombre',
                                            'telefono',
                                            'direccion',
                                            'latitude',
                                            'longitude',
                                            'estado',
                                            'empresa__nombre',
                                            'ciudad__nombre'
                                            ))


    return JsonResponse({'result_list': result_list, 'result_list2': result_list2}, safe=False)




def obtener_Ser_Esp(request):
    nit = request.GET.get('nit', '')  # Obtén el NIT de la empresa desde la solicitud GET
    empresa = Empresas.objects.get(NIT=nit)
    servicios = empresa.servicios.values('nombre').distinct()
    especialidades = empresa.especialidades.values('nombre').distinct()
    lista_servicios = [servicio['nombre'] for servicio in servicios]
    lista_especialidades = [especialidad['nombre'] for especialidad in especialidades]
    return JsonResponse({'servicios': lista_servicios, 'especialidades': lista_especialidades})


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
                busqueda.apennd(completo[idx])
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
            archivo = request.FILES['archivo']
            if archivo:
                uploaded_video = uploader.upload_large(archivo, resource_type='video', chunk_size=6000000)
                p.videoEntrevista = uploaded_video['url']
                p.entrevista = 's'

            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            messages.success(request, "EMPLEADO EXITOSAMENTE CREADO")
            return redirect('map')

        else:

            # Redirect back to the same page if the data
            # was invalid
            messages.error(request, "ERROR EN LA CREACIÓN")
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
    archivo_actual = p.videoEntrevista
    pathEntrevista = p.videoEntrevista if archivo_actual != '' else None
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
            if 'video' in request.FILES:
                archivo_nuevo = request.FILES['video']
                print(archivo_nuevo)
            else:
                archivo_nuevo = None

            if request.POST['uploadFromPC'] != '':
                imagen = encode_file(request.FILES['uploadFromPC'])
                p.imagen = imagen
            # Calcular el límite de tamaño en megabytes
            limite_bytes = 104857600
            limite_mb = limite_bytes / (1024 * 1024)

            if archivo_nuevo.size > limite_bytes:
                print("SE DEVUELVE")
                messages.error(request, "El archivo es demasiado grande. El límite es de 100 MB.")
                return render(request, 'Empleados/editarEmp.html', {'form': form, 'emp': p,'path':pathEntrevista})
            else:
                if archivo_nuevo:
                    print(archivo_nuevo.name)
                    mime_type = tipoContenido(archivo_nuevo.name)
                    print("SACA EL CONTENIDO PUÑETA")
                    type, mime = mime_type.split("/")
                    print(type)
                    uploaded_video = uploader.upload_large(archivo_nuevo, resource_type='video',  chunk_size=6000000)
                    p.videoEntrevista = uploaded_video['url']

                    if archivo_actual:

                        # Eliminar el video existente de Cloudinary
                        public_id = rutaEntrevista(archivo_actual)
                        id, extension = public_id.split(".")
                        mime_type = tipoContenido(archivo_actual)
                        type, mime = mime_type.split("/")
                        print(type)
                        uploader.destroy(id,resource_type='video')
            p.save()
            messages.success(request, "EXITOSAMENTE ACTUALIZADO")

            return redirect('map')
        else:
            form = empleadoForm(instance=p)
            messages.error(request, "ERROR EN LA ACTUALIZACIÓN DE DATOS")
            return render(request, 'Empleados/editarEmp.html', {'form': form, 'emp':p})
    else:
        form = empleadoForm(instance=p)
        return render(request, "Empleados/editarEmp.html", {'form': form, 'emp':p,'path':pathEntrevista})


'''esta función muestra los detalles de un empleado existente en una página separada.'''
@user_login_required
def vistaVerEmpl(request, rest, ced):
    empleados = Empleados.objects.get(documento=ced)
    if empleados.entrevista != 'n':
        #resource_info = cloudinary.api.resource(empleados.videoEntrevista)
        #mime_type = resource_info['resource_type']
        mime_type = tipoContenido(empleados.videoEntrevista)
        context = {
            'emp': rest,
            'empleado': empleados,
            'mime_type': mime_type,
        }
        print("ENTRO")
    else:
        context = {
            'emp': rest,
            'empleado': empleados,
        }
    return render(request, "Empleados/verPersonal.html", context=context)


''' esta función busca un empleado en la base de datos por su número de documento, cambia su estado de "Activo" a "Inactivo" o viceversa, guarda los cambios en la base de datos '''
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


def rutaEntrevista(rutaCompleta):
    parsed_url = urlparse(rutaCompleta)
    ruta_del_archivo_en_el_bucket = parsed_url.path[1:]
    nombre_del_archivo = ruta_del_archivo_en_el_bucket.split('/')[-1]
    return nombre_del_archivo

def tipoContenido(nombreArchivo):
    contenido, encoding = mimetypes.guess_type(nombreArchivo)
    return contenido

@user_login_required
def servicios_especialidades(request):
    servicios = Servicios.objects.all()
    paginator = Paginator(servicios, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'servicios_especialidades/servicios.html', {'page_obj': page_obj})

@user_login_required
def crearServicio(request):
    form = serviciosForm()
    if request.method == 'POST':
        print("HOLAAAAAAAAAAAAAA")
        form = serviciosForm(request.POST)
        if form.is_valid():
            form.save()
            print("Segunda salida")
            return JsonResponse({'success': True, 'message': 'Servicio creado exitosamente.'})
        else:
            print("Tercera salida")
            return JsonResponse({'success': False, 'errors': form.errors})
    print("Primera salida")
    return render(request, 'servicios_especialidades/crearServicio.html', {'form': form})

@user_login_required
def editarServicio(request, servicio_id):
    servicio_id = ObjectId(servicio_id)

    servicio = get_object_or_404(Servicios, _id=servicio_id)
    if request.method == 'POST':
        print("salida entre medio 2")
        form = serviciosForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            print("salida 2")
            return JsonResponse({'success': True, 'message': 'Servicio creado exitosamente.'})
        else:
            print("salida 3")
            return JsonResponse({'success': False, 'errors': form.errors})
    print("salida 1")
    form = serviciosForm(instance=servicio)
    return render(request, 'servicios_especialidades/editarServicio.html', {'form': form})

@csrf_exempt
def eliminarServicio(request, servicio_id):
    servicio_id = ObjectId(servicio_id)
    servicio = get_object_or_404(Servicios, _id=servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return JsonResponse({'success': True, 'message': 'Servicio eliminado exitosamente.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


def especialidades(request):
    especialidades = Especialidades.objects.all()
    paginator = Paginator(especialidades, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'servicios_especialidades/especialidades.html', {'page_obj': page_obj})

@user_login_required
def crearEspecialidad(request):
    form = especialidadesForm()
    if request.method == 'POST':
        print("HOLAAAAAAAAAAAAAA")
        form = especialidadesForm(request.POST)
        if form.is_valid():
            form.save()
            print("Segunda salida")
            return JsonResponse({'success': True, 'message': 'Servicio creado exitosamente.'})
        else:
            print("Tercera salida")
            return JsonResponse({'success': False, 'errors': form.errors})
    print("Primera salida")
    return render(request, 'servicios_especialidades/crearServicio.html', {'form': form})

@user_login_required
def editarEspecialidad(request, servicio_id):
    especialidad_id = ObjectId(servicio_id)

    especialidad = get_object_or_404(Especialidades, _id=especialidad_id)
    if request.method == 'POST':
        print("salida entre medio 2")
        form = especialidadesForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            print("salida 2")
            return JsonResponse({'success': True, 'message': 'Servicio creado exitosamente.'})
        else:
            print("salida 3")
            return JsonResponse({'success': False, 'errors': form.errors})
    print("salida 1")
    form = especialidadesForm(instance=especialidad)
    return render(request, 'servicios_especialidades/editarServicio.html', {'form': form})

@csrf_exempt
def eliminarEspecialidad(request, servicio_id):
    especialidad_id = ObjectId(servicio_id)
    especialidad = get_object_or_404(Especialidades, _id=especialidad_id)
    if request.method == 'POST':
        especialidad.delete()
        return JsonResponse({'success': True, 'message': 'Servicio eliminado exitosamente.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


@user_login_required
def mapaEmp(request, rest):
    user = get_user(request)
    key = settings.GOOGLE_API_KEY
    emp = Empresas.objects.get(nombre=rest)
    context = {
        'key': key,
        'user': user,
        'data': True,
        'lati': emp.latitude,
        'longi': emp.longitude,
        'zoom': 15
    }
    return render(request, 'google/map.html', context)


@user_login_required
def vistaListaEmplTodos(request):
    empleados = Empleados.objects.all()
    user = get_user(request)
    context = {
            'empleados': empleados,
            'user': user,
    }
    return render(request, "Empleados/listaEmpleados.html", context=context)