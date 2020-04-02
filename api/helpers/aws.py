import os

import boto3
from flask import current_app, url_for
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api.config.constants import K


class AWSManager:

    def updateImage(self, image: FileStorage, bucket_path):
        if image:
            return self.save_file(image, bucket_path)
            # image_path, error = self.__upload_files_to_s3(image, K.S3_PROFILE_IMAGE)
            # return image_path if image_path is not None else None
        else:
            return None

    def __upload_files_to_s3(self, file, folder) -> (str, Exception):
        return ('https://homepages.cae.wisc.edu/~ece533/images/airplane.png', None)
        # TODO :- Need to configure if it is working
        s3 = boto3.client(
            "s3",
            aws_access_key_id=current_app.config['S3_KEY'],
            aws_secret_access_key=current_app.config['S3_SECRET']
        )
        bucket = current_app.config['S3_BUCKET']
        random_string = os.urandom(16).hex()
        ext = file.filename.rsplit('.', 1)[1]
        try:
            s3.upload_fileobj(
                file,
                None,
                folder + '/' + random_string + '.' + ext,
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": file.content_type
                }
            )

        except Exception as e:
            return (None, e)

        pathename = folder + '/' + random_string + '.' + ext
        return (pathename, None)

    def __allowed_file(self, filename):
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def save_file(self, file: FileStorage, directory_path: str, uniquename=True):
        if self.__allowed_file(file.filename):
            filename = None
            if uniquename == False:
                filename = secure_filename(file.filename)
            else:
                filename = secure_filename(file.filename)
            file_url = directory_path + filename
            file.save(file_url)
            return file_url
        else:
            raise Exception('Invalid supported format.')

    def delete_file(self, file_path):
        os.remove(file_path)
