import os, uuid
from google.cloud import storage

DIR = os.path.dirname(os.path.realpath(__file__))

class GoogleStorageHelper(object):

    def __init__(self, bucket: str):
        self.bucket_name = bucket
        self.crentials_file = DIR + '/../google.json'
        self.storage_client = storage.Client.from_service_account_json(self.crentials_file)
        self.bucket = self.storage_client.bucket(self.bucket_name)

    def exists(self, filename: str):
        obj = self.bucket.blob(filename)
        return obj if obj.exists() == True else False

    def lists(self):
        blobs = list(self.bucket.list_blobs())
        print("파일 갯수: {}개를 찾았습니다.".format(len(blobs)))

        return blobs
    
    def get(self, filename: str):
        blob = self.exists(filename)
        if blob is False: return None

        location = '/tmp/infra_move_' + filename
        blob.download_to_filename(location)

        return location
