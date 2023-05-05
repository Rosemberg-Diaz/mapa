from asyncio.windows_events import NULL
import googlemaps
import gmaps
from datetime import datetime
from django.shortcuts import render, redirect, reverse
from .forms import *
from .models import *
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.core import serializers
import requests
import json
import urllib
import base64


def encode_file(file):
    # Lee los datos del archivo
    data = file.read()
    # Codifica los datos en Base64
    encoded_data = base64.b64encode(data)
    encoded_string = encoded_data.decode('utf-8')
    return (encoded_string)

# Create your views here.

def home(request):
    context = {}
    return render(request, 'google/home.html',context)


def geocode(request):
    empresa = Empresas.objects.all()
    context = {
        'empresas':empresa,
    }
    return render(request, 'google/geocode.html',context)

#guarda la informacion del formulario en la base de datos
def crearEmpresa(request):
    # check if the request is post
    ciudades = Ciudades.objects.all()
    if request.method == 'POST':

        # Pass the form data to the form class
        details = empresaForm(request.POST)
        print(request.POST['ciudad'])
        # In the 'form' class the clean function
        # is defined, if all the data is correct
        # as per the clean function, it returns true
        if details.is_valid():
            print(request.POST['ciudad'])
            # Temporarily make an object to be add some
            # logic into the data if there is such a need
            # before writing to the database
            post = details.save(commit=False)

            # Finally write the changes into database
            post.save()
            p = Empresas.objects.get(NIT=request.POST['NIT'])
            ciudad = Ciudades.objects.get(nombre=request.POST['ciudad'])
            p.estado = "Activo"
            p.ciudad = ciudad
            p.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return redirect('geocode_club',request.POST['NIT'])

        else:

            # Redirect back to the same page if the data
            # was invalid
            return render(request, "Empresas/create.html", {'form': details, 'ciudades': ciudades})
    else:

        # If the request is a GET request then,
        # create an empty form object and
        # render it into the page
        form = empresaForm(None)
        return render(request, 'Empresas/create.html', {'form': form, 'ciudades': ciudades})

def geocode_club(request,pk):
    empresa = Empresas.objects.get(NIT=pk)
    # check whether we have the data in the database that we need to calculate the geocode
    if empresa.direccion:
        # creating string of existing location data in database
        adress_string = str(empresa.direccion)+', '+str(empresa.ciudad)+", Valle del Cauca, Colombia"
        print(adress_string)

        # geocode the string
        gmaps = googlemaps.Client(key= settings.GOOGLE_API_KEY)
        intermediate = json.dumps(gmaps.geocode(str(adress_string))) 
        intermediate2 = json.loads(intermediate)
        latitude = intermediate2[0]['geometry']['location']['lat']
        longitude = intermediate2[0]['geometry']['location']['lng']
        print(latitude)
        print(longitude)
        # save the lat and long in our database
        empresa.latitude = latitude
        empresa.longitude = longitude
        empresa.save()
        return redirect('map')
    else:
        return redirect('map')
    return render(request, 'google/empty.html',context)


def map(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key':key,
    }
    return render(request, 'google/map.html',context)


def mydata(request):
    result_list = list(Empresas.objects.values('nombre',
                        'latitude',
                        'longitude',
                        'NIT',
                        ))

    return JsonResponse(result_list, safe=False)


def vistaListaEmpl(request, rest):
    emp = Empresas.objects.get(nombre=rest)
    empleados = Empleados.objects.filter(empresa=emp)
    context = {
        'emp': rest,
        'empleados': empleados,
    }
    return render(request, "google/listaEmp.html", context=context)


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
            if (request.POST['video']!=''):
                entrevista = encode_file(request.FILES['video'])
                permisos = encode_file(request.FILES['pdf'])
                p.entrevista = entrevista
                p.permiso = permisos
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



def vistaVerEmpl(request, rest, ced):
    empleados = Empleados.objects.get(documento=ced)
    context = {
        'emp': rest,
        'empleado': empleados,
    }
    return render(request, "Empleados/verPersonal.html", context=context)

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
