from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class MediaRootS3Boto3Storage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = settings.CLOUD_FRONT_DOMAIN