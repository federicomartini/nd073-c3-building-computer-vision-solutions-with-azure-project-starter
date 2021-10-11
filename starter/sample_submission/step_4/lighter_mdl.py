from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os

def find_lighter(img_path):
    
    endpoint = "https://freddycustomvision-prediction.cognitiveservices.azure.com/"
    api_key = "53574aa0b5fd4e97874b541e87b5fbd4"
    project_id = "8a97caa8-4212-4c76-a90a-79818fd07777"

    predictor = CustomVisionPredictionClient(endpoint, ApiKeyCredentials(in_headers={"Prediction-key": api_key}))

    with open(img_path, "rb") as image:
        results = predictor.detect_image(project_id, "Iteration1", image.read())

    return results.predictions[0].probability > 0.65
