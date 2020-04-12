
import json
import requests
import options
import datetime

class ToastToken(object):

    def __init__(self, token: dict):
        self.id = token.get('id', None)
        self.expires = token.get('expires', None)

    def get_token_id(self):
        return self.id
    
    def is_token_expired(self) -> bool:
        if self.expires is None: return True # none이면 무조건 만료됬다고 처리

        now = datetime.datetime.now()
        expiredate = datetime.datetime.strptime(self.expires, '%Y-%m-%dT%H:%M:%SZ')
        
        return now > expiredate

class ToastAuth(object):

    def __init__(self):
        self.auth_url = 'https://api-compute.cloud.toast.com/identity/v2.0'
        self.tenant_id = options.TENANT_ID
        self.username = options.USERNAME
        self.api_password = options.API_PASSWORD

    def get_token(self) -> ToastToken:
        token_url = self.auth_url + '/tokens'
        req_header = {'Content-Type': 'application/json'}
        req_body = {
            'auth': {
                'tenantId': self.tenant_id,
                'passwordCredentials': { 'username': self.username, 'password': self.api_password }
            }
        }
        
        response = requests.post(token_url, headers=req_header, json=req_body)
        if response.status_code == 200:
            token = response.json().get('access', {}).get('token', {})
            return ToastToken(token)
        else:
            return False


class ToastContainerService(object):

    def __init__(self, token_id):
        self.storage_url = options.STORAGE_URL
        self.token_id = token_id

    def get_object_exists(self, name=None):
        req_url = self.storage_url + "/{container}?prefix={name}". \
            format(account=options.ACCOUNT_NAME, container=options.CONTAINER_NAME, name=name)
        header = {'X-Auth-Token': self.token_id}
        res = requests.get(req_url, headers=header)
        if res.status_code == 204:
            return False  # 파일이 없음
        elif res.status_code == 200:
            return True #파일 이있음
        else:
            return None # 무언가 에러.

    def upload_file(self, filename, filepath):
        req_url = '/'.join([self.storage_url, options.CONTAINER_NAME, filename])
        req_header = {'X-Auth-Token': self.token_id}

        with open(filepath, 'rb') as f:
            r = requests.put(req_url, headers=req_header, data=f.read())
            return True if r.status_code == 201 else False
        
        return None