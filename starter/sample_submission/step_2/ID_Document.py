import os
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential
from io import BytesIO

endpoint = "https://freddyformrecognizer1234.cognitiveservices.azure.com/"
key = "2430e68396134e52a482f9eb2ad0b8fe"

def extract_id_data(img_path):
    form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
    
    with open(img_path, "rb") as f:
        image_data = BytesIO(f.read())

        id_documents_recongnizer_result = form_recognizer_client.begin_recognize_identity_documents(image_data).result()

        for recognized_document in id_documents_recongnizer_result:
            first_name = recognized_document.fields.get("FirstName").value
            last_name = recognized_document.fields.get("LastName").value
            dob = recognized_document.fields.get("DateOfBirth").value
            sex = recognized_document.fields.get("Sex").value

        f.close()

    return first_name, last_name, dob, sex

if __name__ == '__main__':
    extract_id_data('./Digital_ID/ca-dl-1.png')