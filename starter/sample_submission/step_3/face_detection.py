from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

KEY = "fea304f9f24f42c4aa1b7b1facb0c928"
ENDPOINT = "https://freddyface1234.cognitiveservices.azure.com/"

face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_face_id(face_image):
    
    faces = face_client.face.detect_with_stream(face_image)
    
    if not faces:
        raise Exception('No faces in the provided image')
    else:
        return faces[0].face_id

def get_face_comparison_confidence(input_face_a, input_face_b):
    
    detected_face_a = get_face_id(input_face_a)
    detected_face_b = get_face_id(input_face_b)
    confidence = face_client.face.verify_face_to_face(detected_face_a, detected_face_b).confidence

    return confidence