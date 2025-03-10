# Ejemplo de uso de Azure AI Services con el SDK de Python
# En este ejemplo, se muestra cómo usar el SDK de Python para Azure AI Services para detectar el idioma de un fragmento de texto.


# Importar las bibliotecas necesarias
from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Variables globales
def main():
    global ai_endpoint
    global ai_key

    try:
        # carga la configuración de un archivo .env
        # para obtener la configuración de la conexión al servicio de análisis de texto
        
        load_dotenv()
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Obtiene la entrada del usuario (hasta que ingrese "quit") 
        userText =''
        while userText.lower() != 'salir':
            userText = input('\n Ingresa tu consulta ("salir" para parar)\n')
            if userText.lower() != 'salir':
                language = GetLanguage(userText)
                print('Language:', language)

    except Exception as ex:
        print(ex)

def GetLanguage(text):


    # Crea el cliente utilizando el punto de conexión
    credential = AzureKeyCredential(ai_key)
    client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)


    # Llama al servico para obtener el idioma detectado
    detectedLanguage = client.detect_language(documents = [text])[0]
    return detectedLanguage.primary_language.name


if __name__ == "__main__":
    main()