# mapa

Esta funcional el crear empresa y el visualizar en el mapa.

Para continuar, en el archivo map.html esta una funcion js OnClick() que son las acciones que se realizan al momento de dar click en el marcador.
Ya esta probada la funcionalidad de conversion de direccion a longitud y latitud, asi que si se van a agregar empresas deben ser con direcciones reales del valle del cauca.

Asi que si voy a agregar una direccion por ejemplo de Cali. Debo escribir la direccion correctamente y seleccionar en el listado de ciudades Cali.


Juan Camilo Clavijo:
Se integro la parte de empleados y empresas, se corrigieron algunas cosas de front y se habilito la visualizacion por parte de los clientes.


INDICACIONES 10/05/2023

Crear al nivel de la carpeta de la aplicacion, una carpeta que se llame "credenciales" e insertar el json correspondiente.

Esta carpeta no se puede subir al repositorio ya que para el almacenamiento de los videos se esta usando google cloud storage y esas credenciales con propias del proyecto, no se deben hacer publicas.

Adicional instalar la siguiente dependencia:
    - pip install django-storages[google]
