# Importe requests y json
import requests
import json

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
# Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required





# Restricción de acceso con @login_required
@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    
    # Arme el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    #print("Endpoint ", url)
    #print("Response ", response_dict)

    # Respuestas totales
    total_responses = len(response_dict.keys())
    
    # Valores de la respuesta
    responses = list(response_dict.values())

    fechas = dict()

    for elemento in responses:
        # Extraer solo la fecha (parte antes de la coma en 'saved')
        fecha = elemento['saved'].split(',')[0]
        fechas.setdefault(fecha,0)
        # Incrementar el conteo para esa fecha
        fechas[fecha] += 1

    # Inicializar variables para el máximo
    fecha_mayor = ""
    cantidad_mayor = 0

    # Iterar sobre el diccionario
    for fecha, cantidad in fechas.items():
        if cantidad > cantidad_mayor:
            fecha_mayor = fecha
            cantidad_mayor = cantidad

    primera_respuesta1 = list(responses)[0]["cedula"]
    primera_respuesta2 = list(responses)[0]["nombre"]

    ultima_respuesta1 = list(responses)[-1]["cedula"]
    ultima_respuesta2 = list(responses)[-1]["nombre"]

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
        'primera_respuesta1' : primera_respuesta1,
        'primera_respuesta2' : primera_respuesta2,
        'ultima_respuesta1' : ultima_respuesta1,
        'ultima_respuesta2' : ultima_respuesta2,
        'fecha_mayor' : fecha_mayor
    }

    # Renderización en la plantilla
    return render(request, 'main/index.html', data)