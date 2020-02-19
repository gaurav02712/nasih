import boto3
from flask import current_app

from api.config.constants import K


class AWSManager:

    def updateImage(self, image):
        if image:
            image_path, error = self.__upload_files_to_s3(image, K.S3_PROFILE_IMAGE)
            return image_path if image_path is not None else None
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
