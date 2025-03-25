# Este archivo
# 1. Carga la configuración de un archivo .env
# 2. Solicita al usuario que ingrese texto
# 3. Llama a un servicio de análisis de texto para determinar el idioma del texto
# 4. Muestra el idioma detectado
# Para mas informacón sobre el uso de los servicios de IA de Azure, consulte el repositorio de GitHub de Microsoft Learning en:
# https://github.com/MicrosoftLearning/AI-102-AIEngineer

# Importar las bibliotecas necesarias

from dotenv import load_dotenv
import os
import http.client, base64, json, urllib
from urllib import request, parse, error

def main():

# Variables globales
    global ai_endpoint
    global ai_key

    try:
        # Get Configuration Settings
        # Carga el archivo .env en el entorno 
        
        load_dotenv()
        
        # para obtener la configuración de la conexión al servicio de análisis de texto
        
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Display the welcome message
        print('Azure AI Text Analytics Service')
        print('================================\n')
        

        # Get user input (until they enter "quit")
        userText =''
        while userText.lower() != 'quit':
            userText = input('\n \n Enter some text ("quit" to stop)\n')
            if userText.lower() != 'quit':
                GetLanguage(userText)


    except Exception as ex:
        print(ex)

def GetLanguage(text):
    try:
        # construye el cuerpo de la solicitud JSON (una colección de documentos, cada uno con un ID y texto)

        jsonBody = {
            "documents":[
                {"id": 1,
                 "text": text}
            ]
        }

        # Analiza el cuerpo de la solicitud JSON
        print(json.dumps(jsonBody, indent=2))

        # Hace una solicitud HTTP a la interfaz REST
        uri = ai_endpoint.rstrip('/').replace('https://', '')
        conn = http.client.HTTPSConnection(uri)

        # Agrega encabezados de solicitud
        # Establece el tipo de contenido en JSON y agrega la clave de suscripción
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ai_key
        }

        # Use the Text Analytics language API
        conn.request("POST", "/text/analytics/v3.1/languages?", str(jsonBody).encode('utf-8'), headers)

        # Send the request
        response = conn.getresponse()
        data = response.read().decode("UTF-8")


        # Si la llamada fue exitosa, obtenga la respuesta
        if response.status == 200:

            # muestra la respuesta JSON analizada 
            results = json.loads(data)
            # print(json.dumps(results, indent=2))
 
            # Extrae el idioma detectado para cada documento
            for document in results["documents"]:
                print("\nLanguage:", document["detectedLanguage"]["name"])

        else:
            # Algo salió mal en la llamada REST - muestra toda la respuesta
            print(data)

        conn.close()


    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()