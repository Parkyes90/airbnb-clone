from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    location = "static/"
    file_overwrite = False


class UploadStorage(S3Boto3Storage):
    def path(self, name):
        pass

    def get_accessed_time(self, name):
        pass

    def get_created_time(self, name):
        pass

    location = "uploads/"
