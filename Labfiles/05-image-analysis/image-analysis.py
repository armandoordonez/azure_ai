from dotenv import load_dotenv
import os
from array import array
from PIL import Image, ImageDraw
import sys
import time
from matplotlib import pyplot as plt
import numpy as np

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials

def main():
    global cv_client

    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Get image
        image_file = 'images/street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate Azure AI Vision client
        credentials = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credentials)

        # Analyze image
        AnalyzeImage(image_file)

        # Generate thumbnail
        GetThumbnail(image_file)

    except Exception as ex:
        print(ex)

def AnalyzeImage(image_file):
    print('Analyzing', image_file)

    # características
    features = ["Description", "Tags", "Objects", "Faces"]

    with open(image_file, "rb") as image_stream:
        analysis = cv_client.analyze_image_in_stream(image_stream , visual_features=features)
    
    if analysis.description.captions:
        print("Description:", analysis.description.captions[0].text)
    if analysis.tags:
        print("Tags:", ", ".join([tag.name for tag in analysis.tags]))
    if analysis.objects:
        print("Objects:", ", ".join([obj.object_property for obj in analysis.objects]))
    if analysis.faces:
        print("Faces detected:", len(analysis.faces))

def GetThumbnail(image_file):
    print('Generating thumbnail')

    

if __name__ == "__main__":
    main()