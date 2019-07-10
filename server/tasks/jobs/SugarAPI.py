import requests
from json import loads, dumps
from json.decoder import JSONDecodeError
import redis

class SugarAPI:
    
    username = ''
    password = ''
    url = ''
    _token = ''
    retry_on_failure = 2
    retried = 0
    cache = False
    redis_url = ''

    def __init__(self, url, username, password, redis_url=None):
        self.url = url
        self.username = username
        self.password = password
        self.redis_url = redis_url
        if self.redis_url  is not None:
            self.cache = True

    def retrieve(module, id):
        pass
    

    @property
    def token(self):
        if not self.cache:
            return self._token
        else:   
            r = redis.Redis.from_url(self.redis_url)
            return r.get('oauth_token')


    @token.setter
    def token(self, val):
        if not self.cache:
            self._token = val
        else:   
            r = redis.Redis.from_url(self.redis_url)
            r.set('oauth_token', val)


    def upsert(self, module:str, payload:dict):

        try:
            method = 'POST'
            if ('id' in payload):
                method = 'PUT'

            payload_ = dumps(payload)
            
            self.token = 'cd6a64b6-2f44-4223-9408-b55b6f685c77'

            url = self.url + "/rest/v11_4/" + str(module).capitalize()
            headers = {
                'origin': self.url,
                'oauth-token': self.token,
                'content-type': "application/json",
                'accept': "application/json, text/javascript, */*; q=0.01",
                'cache-control': "no-cache",
            }
            response = requests.request(method, url, data=payload_, headers=headers)
            resp_ = loads(response.text)
            return resp_

        except JSONDecodeError:
            return False
            
    def rupsert(self, module, payload:dict):
        resp = self.upsert(module, payload)

        if ("error_message" in resp_ 
            and ("No valid authentication for user" in resp_['error_message']
            or "The access token provided is invalid." in resp_['error_message'])
            ):
                if self.retried >= self.retry_on_failure:
                    return False

                self.authenticate()
                self.retried += 1
                return self.rupsert(module, payload)
        
        return resp



    def authenticate(self):
        url = self.url + "/rest/v11_4/oauth2/token"
        querystring = {"platform":"base"}
        payload = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "client_id":"sugar",
            "platform":"base",
            "client_secret":"",
            "current_language":
            "en_us",
            "client_info":{
                "current_language":"en_us"
            }
        }
        payload = dumps(payload)
        headers = {
            'accept': "application/json, text/javascript, */*; q=0.01",
            'x-requested-with': "XMLHttpRequest",
            'content-type': "application/json",
        }
        response = requests.request(
            "POST", 
            url, 
            data=payload, 
            headers=headers, 
            params=querystring
        )
        
        response_ = response.text
        
        try:
            if 'access_token' in response_:
                json_resp = loads(response_)
                self.token = json_resp['access_token']
                return True
        except JSONDecodeError:
            pass

        return False
    
    def delete(module, record):
        pass
    
    def isAuthenticated():
        pass
    
if __name__ == '__main__':
    s = SugarAPI(
        'https://OURS.sugarondemand.com', 
        'UN', 
        'PW',
        'redis://localhost:6379/0'
    )
    s.authenticate()
    print(s.upsert('Tasks', {'name': "A new task"}))