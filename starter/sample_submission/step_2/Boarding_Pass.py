import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient

class BoardingPass(object):

    endpoint = 'https://freddyformrecognizer1234.cognitiveservices.azure.com/'
    key = '2430e68396134e52a482f9eb2ad0b8fe'
    model_id = '61668e64-a414-43e8-a3f9-33b391626642'

    def get_flight_details_from_custom_Form(self, bp_path):
        
        #Init the flight details dict as empty
        flight_details = {}

        with open(bp_path, "rb") as f:
            form_recognizer_client = FormRecognizerClient(
            endpoint=self.endpoint, credential=AzureKeyCredential(self.key)).begin_recognize_custom_forms(
                model_id=self.model_id, form=f, include_field_elements=True, content_type='application/pdf')

        form_recognizer_client_result = form_recognizer_client.result()

        for form in form_recognizer_client_result:
            for name, field in form.fields.items():

                if field.label_data:
                    key = field.label_data.text
                else:
                    key = name

                flight_details[key] = field.value

        return flight_details