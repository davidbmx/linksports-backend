from django.conf import settings
import firebase_admin
from firebase_admin import credentials, auth

try:
    app = firebase_admin.get_app()
except ValueError as e:
    # if settings.PRODUCTION:
        # file_name = str(settings.ROOT_DIR.path('private.json'))
    # else:
    print(settings.BASE_DIR)
    file_name = str(f"{settings.BASE_DIR}/linksports-82679-827b47fee510.json")
    cred = credentials.Certificate(file_name)
    firebase_admin.initialize_app(cred)

