from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

from firebase_admin import db

class LandingAPI(APIView):
    
    name = 'Landing API'

    # Coloque el nombre de su colección en el Realtime 
    collection_name = 'data'
    
    def get(self, request):

        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')
        
        # get: Obtiene todos los elementos de la colección
        data = ref.get()

        # Devuelve un arreglo JSON
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        
        # Referencia a la colección
        ref = db.reference(f'{self.collection_name}')

        current_time  = datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        request.data.update({"saved": custom_format })
        
        # push: Guarda el objeto en la colección
        new_resource = ref.push(request.data)
        
        # Devuelve el id del objeto guardado
        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)

class LandingAPIDetail(APIView):

    name = 'Landing Detail API'

    collection_name = 'data'

    def get(self, request, pk):                
        ref = db.reference(f'{self.collection_name}/{pk}')                
        document = ref.get()
        
        if document is None:
            return Response({"error": "Documento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        # Si el documento existe, retornar los datos con status 200 OK
        return Response(document, status=status.HTTP_200_OK)

    def put(self, request, pk):
        ref = db.reference(f'{self.collection_name}/{pk}')
        
        datos = ref.get()
        #verificar si el recurso existe
        if datos is None:
            return Response({"error":"Dato no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        if not request.data:
            return Response({"error": "El cuerpo de la solicitud está vacío"}, status=status.HTTP_400_BAD_REQUEST)
        # Actualizar los datos del documento
        ref.update(request.data)
         # Devolver un mensaje confirmando la actualización
        return Response({"message": "Documento actualizado exitosamente"}, status=status.HTTP_200_OK)

        

    def delete(self, request, pk):
         ref = db.reference(f'{self.collection_name}/{pk}')
         
         dato = ref.get()
         
         if dato is None:
             return Response({"eror": "Dato no encontrado"}, status=status.HTTP_404_NOT_FOUND)
         # Eliminamos la referencia
         ref.delete()
         return Response({"messege": "Dato eliminado exitosamente"},status=status.HTTP_204_NO_CONTENT)