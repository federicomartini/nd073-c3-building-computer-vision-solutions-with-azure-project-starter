'''
The whole snippet is available in the official documentation in the "Train a model" paragraph: 
https://docs.microsoft.com/en-us/python/api/overview/azure/ai-formrecognizer-readme?view=azure-python
'''

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
from azure.ai.formrecognizer import FormTrainingClient

endpoint = "https://freddyformrecognizer1234.cognitiveservices.azure.com/"
credential = AzureKeyCredential("2430e68396134e52a482f9eb2ad0b8fe")
# training documents uploaded to blob storage
container_sas_url = "https://freddystorageaccount123.blob.core.windows.net/boardingpass?sp=racwdl&st=2021-10-10T17:33:24Z&se=2021-10-31T17:33:00Z&sv=2020-08-04&sr=c&sig=PSA%2BffxPRGKzKfdkvQ%2F9jcrza2P1FxWujT82viiIO3k%3D"

form_training_client  = FormTrainingClient(endpoint, credential)

poller = form_training_client.begin_training(
    container_sas_url, use_training_labels=True, model_name="BoardingPassRecognizer"
)
model = poller.result()

# Custom model information
print("Model ID: {}".format(model.model_id))
print("Model name: {}".format(model.model_name))
print("Is composed model?: {}".format(model.properties.is_composed_model))
print("Status: {}".format(model.status))
print("Training started on: {}".format(model.training_started_on))
print("Training completed on: {}".format(model.training_completed_on))

print("\nRecognized fields:")
for submodel in model.submodels:
    print(
        "The submodel with form type '{}' and model ID '{}' has recognized the following fields: {}".format(
            submodel.form_type, submodel.model_id,
            ", ".join(
                [
                    field.label if field.label else name
                    for name, field in submodel.fields.items()
                ]
            ),
        )
    )

# Training result information
for doc in model.training_documents:
    print("Document name: {}".format(doc.name))
    print("Document status: {}".format(doc.status))
    print("Document page count: {}".format(doc.page_count))
    print("Document errors: {}".format(doc.errors))
