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
from bson.objectid import ObjectId
#Importaciones para cloud storage
from google.cloud import storage
from django.conf import settings
import os
from urllib.parse import urlparse
import mimetypes


"""
Vista de registro de usuario en la pagina web.

Métodos:

registro(request)
    Esta función maneja las solicitudes GET y POST de la vista de registro de usuario.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

HttpResponseRedirect
    Redirige al usuario a la página de inicio si la creación de usuario es exitosa.
    Si hay un error en la creación del usuario, se renderiza la plantilla registro.html con un mensaje de error.
"""


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


"""
Vista de inicio de sesión en la pagina web.

Métodos:

login(request)
    Esta función maneja las solicitudes GET y POST de la vista de inicio de sesión.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

HttpResponse
    Si la autenticación es exitosa, redirige al usuario a la página de map.
    Si hay un error en la autenticación, renderiza la plantilla login.html con un mensaje de error.
"""


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



"""
Obtiene el objeto Usuario correspondiente al usuario actualmente autenticado.

Métodos:

get_user(request)
    Esta función obtiene el ID del usuario de la sesión actual y devuelve el objeto Usuario correspondiente.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

Usuarios
    Objeto Usuario correspondiente al usuario actualmente autenticado.
"""

def get_user(request):
    user_id = request.session.get('user_id')
    user_id = ObjectId(user_id)
    return Usuarios.objects.get(pk=user_id)


"""
Vista base de la pagina web.

Métodos:

vistaBase(request)
    Esta función renderiza la plantilla base.html.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

HttpResponse
    Renderiza la plantilla base.html.
"""

def vistaBase(request):
    return render(request, "Autenticacion/base.html")


"""
Vista de cierre de sesión en la pagina web.

Métodos:

logout_view(request)
    Esta función maneja la solicitud GET de la vista de cierre de sesión.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

HttpResponseRedirect
    Redirige al usuario a la página de inicio después de cerrar la sesión.
"""


@user_login_required
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # delete user session
    return redirect('inicio')



"""
Vista de página principal de la pagina web.

Métodos:

home(request)
    Esta función renderiza la plantilla home.html.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

HttpResponse
    Renderiza la plantilla home.html.
"""


@user_login_required
def home(request):
    context = {}
    return render(request, 'google/home.html', context)



"""
Vista de geocodificación de la pagina web.

Métodos:

geocode(request)
    Esta función renderiza la plantilla geocode.html con la información de todas las empresas.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

HttpResponse
    Renderiza la plantilla geocode.html con la información de todas las empresas.
"""

@user_login_required
def geocode(request):
    empresa = Empresas.objects.all()
    context = {
        'empresas': empresa,
    }
    return render(request, 'google/geocode.html', context)


"""
Vista de creación de empresa de la pagina web.

Métodos:

crearEmpresa(request)
    Esta función maneja las solicitudes GET y POST de la vista de creación de empresa.

Parámetros:

request : HttpRequest
    Objeto HttpRequest que contiene información sobre la solicitud.

Retorna:

HttpResponseRedirect o HttpResponse
    - Si la solicitud es POST y los datos del formulario son válidos, la vista crea la empresa y redirige al usuario a la vista geocode_club.
    - Si la solicitud es POST y los datos del formulario no son válidos, la vista muestra el formulario con los errores.
    - Si la solicitud es GET, la vista muestra el formulario vacío para crear una nueva empresa.
"""


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
            messages.success(request, "EMPRESA EXITOSAMENTE CREADA")
            return redirect('geocode_club', request.POST['NIT'])
        else:
            messages.error(request, "ERROR EN LA CREACIÓN")
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
#             messages.sucess(request, "EXITOSAMENTE CREADO")
#             return redirect('geocode_club', request.POST['nombre'])
#         else:
#             messages.error(request, "ERROR EN LA CREACIÓN")
#             return render(request, "Sedes/create.html", {'form': details, 'ciudades': ciudades, 'empresas': empresas})
#     else:
#         form = sedeForm(None)
#         messages.error(request, "ERROR EN LA CREACIÓN")
#         return render(request, 'Sedes/create.html', {'form': form, 'ciudades': ciudades, 'empresas': empresas})



"""
    Recibe una petición HTTP GET o POST y un NIT (número de identificación tributaria) de una empresa.
    Si la petición es GET, se obtiene la empresa con el NIT proporcionado, se crea un formulario empresaForm con los datos de la empresa 
    y se muestra la plantilla 'Empresas/edit.html', que renderiza el formulario y permite modificar los datos de la empresa. 
    Si la petición es POST, se valida el formulario, se actualiza la empresa con los datos proporcionados en el formulario 
    y se redirige al usuario a la vista 'geocode_club' con el NIT de la empresa actualizado. 
    Si el formulario no es válido, se muestra un mensaje de error y se vuelve a renderizar la plantilla con el formulario y los datos de la empresa 
    para que el usuario pueda corregir los errores.

    Parámetros:
    
    - request: objeto HttpRequest con los datos de la solicitud HTTP.
    - NIT: número de identificación tributaria de la empresa a editar.

    Retorna:
    
    - objeto HttpResponse con la plantilla renderizada.
"""

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
            messages.success(request, "EXITOSAMENTE ACTUALIZADO")
            return redirect('geocode_club', empresa.NIT)
        else:
            messages.error(request, "ERROR EN LA ACTUALIZACIÓN DE DATOS")
            return render(request, "Empresas/edit.html", {'form': form, 'ciudades': ciudades, 'nit': NIT, 'empresa':empresa})
    else:
        form = empresaForm(instance=empresa)
        return render(request, 'Empresas/edit.html', {'form': form, 'ciudades': ciudades, 'nit': NIT, 'empresa':empresa})




"""
    Esta función recibe una solicitud y el NIT de una empresa a inactivar.
    Utilizando el NIT, se obtiene la empresa utilizando la función get_object_or_404.
    Luego, se establece el estado de la empresa en False y se guarda el registro en la base de datos.
    Finalmente, se envía un mensaje de éxito y se redirige al usuario a la página geocode_club de la empresa en cuestión.

    Parámetros:
    
    - request: la solicitud HTTP recibida.
    - NIT: el NIT de la empresa a inactivar.

    Retorna:
    
    - Una redirección a la página geocode_club de la empresa inactivada.
"""

def inactivarEmpresa(request, NIT):
    empresa = get_object_or_404(Empresas, NIT=NIT)
    empresa.estado = False
    empresa.save()
    messages.success(request, "LA EMPRESA SE INACTIVO CORRECTAMENTE")
    return redirect('geocode_club', empresa.NIT)


"""
    Toma un objeto request y un parámetro pk que es el NIT de una empresa,
    y utiliza la API de Google Maps para obtener las coordenadas de la ubicación de la empresa
    y almacenarlas en la base de datos. Si los datos de la ubicación ya están en la base de datos,
    simplemente redirige al usuario a una página de mapa.

    Parámetros:
    
        request: objeto HttpRequest que representa la solicitud HTTP que se está procesando.
        pk (str): NIT de la empresa.

    Retorna:
    
        HttpResponseRedirect o HttpResponse: redirecciona al usuario a una página de mapa si los datos de ubicación
        de la empresa ya están en la base de datos, o a una página vacía si se obtuvieron las coordenadas exitosamente.
"""

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


"""
   Renderiza un template con un mapa de Google Maps y permite buscar una empresa específica para mostrar su ubicación en el mapa.

   Parámetros:

   request -- Solicitud HTTP.

   Retorna:

   Respuesta HTTP con un mapa de Google Maps.

"""

@user_login_required
def mapa(request):
    user = get_user(request)
    print(user.pk)
    key = settings.GOOGLE_API_KEY
    empres =  Empresas.objects.all()
    nombres= []
    for i in empres:
        print(empres)
        nombres.append(i.nombre)
    print(nombres)
    if request.method == 'POST':
        if request.POST['search'] in nombres:
            emp = Empresas.objects.get(nombre=request.POST['search'])
            context = {
                'key': key,
                'user': user,
                'lati': emp.latitude,
                'longi': emp.longitude,
                'Empresa': emp,
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
    else:
        context = {
            'key': key,
            'user': user,
            'lati': 3.43722,
            'longi': -76.5225,
            'zoom': 12
        }
    return render(request, 'google/map.html', context)


"""
    Recupera información de todas las empresas de la base de datos y la convierte en una lista de diccionarios que contienen
    los valores de los campos seleccionados. Luego, devuelve una respuesta JSON con esta lista.
    
    Parámetros:
    
        request (HttpRequest): objeto HttpRequest que representa la solicitud HTTP que se está procesando.
        
    Retorna:
    
        JsonResponse: respuesta HTTP con una lista de diccionarios que contienen información de las empresas en formato JSON.
"""

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



"""
    Renderiza una plantilla HTML que muestra una lista de empleados asociados a una empresa con un nombre dado.
    La lista se puede filtrar por nombre completo de empleado mediante una búsqueda.

    Argumentos:
    
    - request: solicitud HTTP recibida.
    - rest: nombre de la empresa de la cual se quiere obtener la lista de empleados.

    Retorna:
    
    - Un objeto HttpResponse que contiene la respuesta HTTP resultante.
"""

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


"""
    Codifica el contenido de un archivo en Base64.

    Argumentos:
    - file: objeto File del cual se obtendrá el contenido a codificar.

    Retorna:
    - encoded_string: cadena de texto que representa el contenido del archivo
                      codificado en Base64.
"""

def encode_file(file):
    # Lee los datos del archivo
    data = file.read()
    # Codifica los datos en Base64
    encoded_data = base64.b64encode(data)
    encoded_string = encoded_data.decode('utf-8')
    return (encoded_string)


"""
    Crea un nuevo empleado y lo agrega a la base de datos.

    Argumentos:
        request (HttpRequest): solicitud HTTP.
        rest (str): nombre de la empresa.

    Retorna:
        HttpResponse: respuesta HTTP que redirige a la página del mapa o renderiza el formulario.
"""

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
                # Crear el cliente de almacenamiento de Google Cloud
                client = storage.Client.from_service_account_json(os.path.join(settings.CREDENCIALES_DIR, 'high-task-380101-567919917d93.json'))
                # Obtener el bucket
                bucket = client.get_bucket(settings.GS_BUCKET_NAME)
                # Crear el nombre del archivo usando el ID del empleado y el nombre del archivo original
                archivo_nombre = f"{p.pk}-{archivo.name}"

                blob = bucket.blob(archivo_nombre, chunk_size=10*1024*1024)
                content_type = tipoContenido(archivo.name)

                blob.upload_from_file(
                    archivo,
                    content_type=content_type,
                    size=archivo.size,
                    num_retries=5,
                    timeout=120,
                )

                p.videoEntrevista = f"https://storage.googleapis.com/{bucket.name}/{archivo_nombre}"
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


"""
    Actualiza la información de un empleado existente en la base de datos.

    Argumentos:
    - request: objeto HttpRequest de Django
    - rest: nombre de la empresa del empleado (str)
    - ced: número de documento del empleado (str)

    Retorna:
    - Si el método de solicitud es 'POST' y el formulario es válido, redirige al usuario a la página principal del sitio web.
    - Si el método de solicitud es 'POST' y el formulario no es válido, muestra un mensaje de error y redirige al usuario a la página de edición de empleado.
    - Si el método de solicitud no es 'POST', muestra el formulario de edición de empleado con la información actual del empleado.
"""

@user_login_required
def vistaEditarEmpl(request, rest, ced):
    p = Empleados.objects.get(documento=ced)
    archivo_actual = p.videoEntrevista
    pathEntrevista = rutaEntrevista(archivo_actual) if archivo_actual != '' else None
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

            if archivo_nuevo:
                print("entro al archivo")
                client = storage.Client.from_service_account_json(
                    os.path.join(settings.CREDENCIALES_DIR, 'high-task-380101-567919917d93.json'))
                bucket = client.get_bucket(settings.GS_BUCKET_NAME)
                archivo_nombre = f"{p.pk}-{archivo_nuevo.name}"
                blob = bucket.blob(archivo_nombre, chunk_size=10 * 1024 * 1024)
                content_type = tipoContenido(archivo_nuevo.name)

                blob.upload_from_file(
                    archivo_nuevo,
                    content_type=content_type,
                    size=archivo_nuevo.size,
                    num_retries=5,
                    timeout=120,
                )
                p.videoEntrevista = f"https://storage.googleapis.com/{bucket.name}/{archivo_nombre}"
                if archivo_actual:
                    blob_actual = bucket.blob(pathEntrevista)
                    blob_actual.delete()

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


"""
   Muestra los datos de un empleado y su video de entrevista, si tiene.

   Argumentos:
       request: HttpRequest, objeto que contiene información sobre la solicitud web actual.
       rest: str, parámetro correspondiente al nombre del restaurante.
       ced: str, parámetro correspondiente al documento de identificación del empleado.

   Retorna:
       HttpResponse con un template HTML que muestra los datos del empleado y el video de entrevista, si tiene.
"""

@user_login_required
def vistaVerEmpl(request, rest, ced):
    empleados = Empleados.objects.get(documento=ced)
    if empleados.entrevista != 'n':
        # Obtener instancia del cliente de Cloud Storage
        client = storage.Client.from_service_account_json(
            os.path.join(settings.CREDENCIALES_DIR, 'high-task-380101-567919917d93.json'))
        # Obtener instancia del objeto Bucket
        bucket = client.get_bucket(settings.GS_BUCKET_NAME)
        path = rutaEntrevista(empleados.videoEntrevista)
        blob = bucket.get_blob(path)
        mime_type = blob.content_type
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


"""
    Cambia el estado de un empleado de "Activo" a "Inactivo" o viceversa.

    Argumentos:
    - request: objeto HttpRequest que representa la solicitud HTTP que se está procesando.
    - rest: variable que representa el establecimiento al que pertenece el empleado.
    - ced: variable que representa el número de documento del empleado.

    Retorna:
    - Un objeto HttpResponse que redirige al usuario a la página "map".
"""

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


"""
    Devuelve el nombre del archivo dado una ruta completa de un archivo almacenado en un bucket de Google Cloud Storage.

    Argumentos:
    rutaCompleta (str): La ruta completa de un archivo almacenado en un bucket de Google Cloud Storage.

    Retorna:
    str: El nombre del archivo.
"""

def rutaEntrevista(rutaCompleta):
    parsed_url = urlparse(rutaCompleta)
    ruta_del_archivo_en_el_bucket = parsed_url.path[1:]
    nombre_del_archivo = ruta_del_archivo_en_el_bucket.split('/')[-1]
    return nombre_del_archivo


"""
    Devuelve el tipo de contenido MIME de un archivo.

    Args:
    nombreArchivo (str): El nombre del archivo o su extensión.

    Returns:
    str: El tipo de contenido MIME del archivo.
"""


def tipoContenido(nombreArchivo):
    contenido, encoding = mimetypes.guess_type(nombreArchivo)
    return contenido