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


# Create your views here.

def home(request):
    context = {}
    return render(request, 'google/home.html', context)


def geocode(request):
    empresa = Empresas.objects.all()
    context = {
        'empresas': empresa,
    }
    return render(request, 'google/geocode.html', context)


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



def editarEmpresa(request, NIT):
    empresa = get_object_or_404(Empresas, NIT=NIT)
    ciudades = Ciudades.objects.all()

    if request.method == 'POST':
        form = empresaForm(request.POST, instance=empresa)
        if form.is_valid():
            nit = request.POST['NIT']
            valor = int(nit)
            if valor not in range(100000000, 1000000000):
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


def map(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key': key,
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


def vistaListaEmpl(request):
    return render(request, "google/listaEmp.html")


def vistaCrearEmpl(request):
    return render(request, "Empleados/crearEmp.html")


def vistaEditarEmpl(request):
    return render(request, "Empleados/editarEmp.html")


def vistaVerEmpl(request):
    return render(request, "Empleados/verPersonal.html")
