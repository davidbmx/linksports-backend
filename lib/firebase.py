from django.conf import settings
import firebase_admin
from firebase_admin import credentials, auth
from google.cloud import storage
from google.oauth2 import service_account
from io import BytesIO

BUCKET_NAME = 'linksports-82679.appspot.com'
file_name = str(f"{settings.BASE_DIR}/linksports-82679-827b47fee510.json")


try:
    app = firebase_admin.get_app()
except ValueError as e:
    # if settings.PRODUCTION:
        # file_name = str(settings.ROOT_DIR.path('private.json'))
    # else:
    cred = credentials.Certificate(file_name)
    firebase_admin.initialize_app(cred)

def upload_image_to_firebase(file_path, destination_path):
    """
    Carga una imagen en Firebase Storage.

    Args:
    - file_path (str): Ruta al archivo de imagen local.
    - bucket_name (str): Nombre del bucket de Firebase Storage.
    - destination_path (str): Ruta de destino en Firebase Storage.

    Returns:
    - str: URL de descarga de la imagen cargada.
    """
    credentials = service_account.Credentials.from_service_account_file(file_name)
    # Crea un cliente de almacenamiento de Google Cloud
    storage_client = storage.Client(credentials=credentials)

    # Obtén un enlace de URL de Firebase Storage
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_path)



    blob.upload_from_file(file_path, content_type=file_path.content_type)

    # Obtén la URL de descarga de la imagen
    download_url = blob.public_url

    return download_url

