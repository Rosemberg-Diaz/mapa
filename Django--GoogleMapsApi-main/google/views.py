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


# Create your views here.
def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        contraseña = request.POST['clave']
        email = request.POST['email']
        Usuarios.objects.create_user(email, username, contraseña)
        return redirect('inicio')
    else:
        return render(request, 'Autenticacion/registro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        contraseña = request.POST['contraseña']
        user = CustomAuthBackend().authenticate(
            request, email=email, contraseña=contraseña)

        print(user.pk)
        if user is not None:
            request.session['user_id'] = str(user.pk)
            return redirect('map')

        else:
            error_message = 'Nombre de usuario o contraseña incorrectos'
    else:
        error_message = None
    return render(request, 'Autenticacion/login.html', {'error_message': error_message})

def get_user(request):
    user_id = request.session.get('user_id')
    user_id = ObjectId(user_id)
    return Usuarios.objects.get(pk=user_id)


def vistaBase(request):
    return render(request, "Autenticacion/base.html")

@user_login_required
def logout_view(request):
    if 'user_id' in request.session:
        del request.session['user_id']  # delete user session
    return redirect('inicio')



# Create your views here.
@user_login_required
def home(request):
    context = {}
    return render(request, 'google/home.html', context)

@user_login_required
def geocode(request):
    empresa = Empresas.objects.all()
    context = {
        'empresas': empresa,
    }
    return render(request, 'google/geocode.html', context)

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

@user_login_required
def crearSede(request):
    ciudades = Ciudades.objects.all()
    empresas = Empresas.objects.all()
    if request.method == 'POST':
        details = sedeForm(request.POST)
        if details.is_valid():
            nombre = request.POST['nombre']
            post = details.save(commit=False)
            post.save()
            p = Sedes.objects.get(nombre=nombre)
            ciudad = Ciudades.objects.get(nombre=request.POST['ciudad'])
            empresa = Empresas.objects.get(nombre=request.POST['empresa'])
            p.ciudad = ciudad
            p.empresa = empresa
            p.save()
            return redirect('geocode_club', request.POST['nombre'])
        else:
            return render(request, "Sedes/create.html", {'form': details, 'ciudades': ciudades, 'empresas': empresas})
    else:
        form = sedeForm(None)
        return render(request, 'Sedes/create.html', {'form': form, 'ciudades': ciudades, 'empresas': empresas})


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


def inactivarEmpresa(request, NIT):
    empresa = get_object_or_404(Empresas, NIT=NIT)
    empresa.estado = False
    empresa.save()
    return redirect('geocode_club', empresa.NIT)

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

@user_login_required
def mapa(request):
    user = get_user(request)
    print(user.pk)
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
        'user': user
    }
    return render(request, 'google/map.html', context)


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

@user_login_required
def vistaListaEmpl(request, rest):
    emp = Empresas.objects.get(nombre=rest)
    empleados = Empleados.objects.filter(empresa=emp)
    user = get_user(request)
    context = {
        'emp': rest,
        'empleados': empleados,
        'user':user,
    }
    return render(request, "google/listaEmp.html", context=context)

def encode_file(file):
    # Lee los datos del archivo
    data = file.read()
    # Codifica los datos en Base64
    encoded_data = base64.b64encode(data)
    encoded_string = encoded_data.decode('utf-8')
    return (encoded_string)

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