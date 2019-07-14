import requests
from json import loads, dumps
from json.decoder import JSONDecodeError
import redis
import datetime

import sys
from time import sleep

#import asyncio

class SugarAPI:
    
    username = ''
    password = ''
    url = ''
    _token = None
    retry_on_failure = 2
    retried = 0
    cache = False
    redis_url = 'redis://sip_redis:6379/0'
    oauth_token_place_holder = 'oauth_token'

    def __init__(self, url, username, password, redis_url=None, oauth_token_place_holder='oauth_token'):
        
        #self.token = None

        self.url = url
        self.username = username
        self.password = password
        self.redis_url = redis_url
        self.oauth_token_place_holder = oauth_token_place_holder
        if self.redis_url  is not None:
            self.cache = True
        


    def retrieve(self, module, id):
        pass
    

    def __token_yeilder(self):
        #format it since redis only accepts byte, string or number
        if not self.cache:
            access_token_ = self._token
        else:   
            r = redis.Redis.from_url(self.redis_url)
            access_token_ = r.get(self.oauth_token_place_holder)
        
        try:
            access_token_ = loads(str(access_token_))
        except JSONDecodeError:
            pass

        if (type(access_token_) is bytes):
            access_token_ = access_token_.decode('ascii')
            access_token_ = loads(access_token_)

        return access_token_

    @property
    def token(self):

        access_token_ = self.__token_yeilder()
        current_time_stamp = datetime.datetime.now().timestamp()
        #current_time_stamp = 1562953555.385923
        
        

        print(access_token_)
        type(type(access_token_) is dict)
        try:
            if self.retried >= self.retry_on_failure:
                print('Maximum tries done! Couldnt get the oauth token')
                self.token = '' #setting empty so next call will try to authenticate
                raise RuntimeError

            elif type(access_token_) is dict and "status" in access_token_ and access_token_['status'] == 'wait':
                print('authentication token generation is in progress!')
                while True:
                    print('Going to sleep for some time')
                    sleep(3)
                    print('Checking if its still waiting')
                    if access_token_['status'] == 'wait' and float(current_time_stamp) > (float(access_token_["started"]) + float(access_token_["expires_in"])):
                        print('waiting time check has exceeded. something would have gone wrong!')
                        self.token = ''
                        return None
                    else:
                        return self.token
                        

            elif type(access_token_) is dict and 'status' in access_token_ and access_token_['status'] == 'broken':
                print('authentication token generation has been broken due to some server error!')
                self.__authenticate()
                return self.token

            elif type(access_token_) is dict and 'expires_in' in access_token_  and float(current_time_stamp) > (float(access_token_["started"]) + float(access_token_["expires_in"])):
                #the token has expired. Call the 
                print('The token has expired. Authenticating again')
                self.__authenticate()
                return self.token
            
            elif type(access_token_) is dict and 'access_token' in access_token_:
                print('we have a working live oauth token!')
                print('current time stamp', current_time_stamp)
                print('expires by', float(access_token_["started"]) + float(access_token_["expires_in"]))
                
                expires_in = ((float(access_token_["started"]) + float(access_token_["expires_in"])) - current_time_stamp) / 60 
                print('expires in ', expires_in, ' minutes')

                return access_token_['access_token']

            elif type(access_token_) is dict and 'error' in access_token_:
                print("Last time we must have got 'error': 'need_login'")
                self.__authenticate()
                return self.token

            elif not access_token_:
                print('its time to generate an auth for first time')
                #its time to generate an auth for first time
                self.__authenticate()
                return self.token

            else:
                return None
        except ValueError as e:
            print(e)
            print('Invalid auth details found on cache!')
            print('Going to reauthenticate!')
            self.__authenticate()
            return self.token

    def generate_token(self):
        

        print('requesting a token')
        waiting_time_refresh_token = 60 * 2 #2 mins
        current_timstamp = datetime.datetime.now().timestamp()
        self.token = dumps({"status":"wait", "started": str(current_timstamp), "expires_in":waiting_time_refresh_token})
        
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
        self.retried += 1
        resp_ =  requests.request(
            "POST", 
            url, 
            data=payload, 
            headers=headers, 
            params=querystring
        )
        return resp_

    def __authenticate(self):
        

        current_timstamp = datetime.datetime.now().timestamp()
        response_ = self.generate_token()
        print(response_.text)
        try:
            if 'access_token' in response_.text:
                json_resp = loads(response_.text)
                json_resp['started'] = str(current_timstamp)
                self.token = dumps(json_resp)
                return True
            else:
                self.token = dumps({'status':'broken'})
        except JSONDecodeError:
            self.token = dumps({'status':'broken'})
            pass

        return False


    @token.setter
    def token(self, val):
        if not self.cache:
            self._token = val
        else:
            r = redis.Redis.from_url(self.redis_url)
            r.set(self.oauth_token_place_holder, val)

    def upsert(self, module:str, payload:dict):

        try:
            method = 'POST'
            if ('id' in payload):
                method = 'PUT'

            payload_ = dumps(payload)
            
            #self.token = 'cd6a64b6-2f44-4223-9408-b55b6f685c77'

            url = self.url + "/rest/v11_4/" + str(module).capitalize()
            headers = {
                'origin': self.url,
                'oauth-token': str(self.token),
                'content-type': "application/json",
                'accept': "application/json, text/javascript, */*; q=0.01",
                'cache-control': "no-cache",
            }
            #return ''
            response = requests.request(method, url, data=payload_, headers=headers)
            resp_ = loads(response.text)
            print(self.token)
            print(response.status_code)
            if (response.status_code == 200):
                return resp_
            elif 'The access token provided is invalid' in response.text:
                self.token = dumps({'status':'broken'})
            #need to raise exception 
            raise RuntimeError

        except JSONDecodeError:
            return False
            
    def upsert_with_retries(self, module, payload:dict):
        resp_ = self.upsert(module, payload)

        if ("error_message" in resp_ 
            and ("No valid authentication for user" in resp_['error_message']
            or "The access token provided is invalid." in resp_['error_message'])
        ):
            if self.retried >= self.retry_on_failure:
                return False

            self.__authenticate()
            self.retried += 1
            return self.upsert_with_retries(module, payload)
        
        return resp_
    
    def delete(self, module, record):
        pass
    
    def isAuthenticated(self):
        pass
    
if __name__ == '__main__':

    

    '''
    s = SugarAPI(
        'https://X.sugarondemand.com', 
        'X', 
        'Y',
        'redis://sip_redis:6379/0'
    )

    print(s.upsert('Tasks', {'name': "A new task"}))
    '''

    '''
    def request_for_token():
        url =   "https://X.sugarondemand.com/rest/v11_4/oauth2/token"
        querystring = {"platform":"base"}
        payload = {
            "grant_type": "password",
            "username": 'X',
            "password": 'Y',
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

        resp_ = requests.request(
            "POST", 
            url, 
            data=payload, 
            headers=headers, 
            params=querystring
        )
        return resp_

    request_for_token()

    '''

    '''
    @asyncio.coroutine
    def generate_token():
        waiting_time_refresh_token = 60 * 2 #2 mins
        current_timstamp = datetime.datetime.now().timestamp()
        #self.token = dumps({"status":"wait", "started": str(current_timstamp), "expires_in":waiting_time_refresh_token})
        
        
        
        loop = asyncio.get_event_loop()
        resp = loop.run_in_executor(None, request_for_token)
        resp_ = yield from resp

        print(resp_.text)
        return dumps(resp_.text)
        
    #asyncio.run(generate_token())
    '''

    '''
    @asyncio.coroutine
    def main():
        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
        future2 = loop.run_in_executor(None, requests.get, 'http://www.google.co.uk')
        response1 = yield from future1
        response2 = yield from future2
        print(response1.text)
        print(response2.text)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print('ddd')
    '''
    
    '''
    loop = asyncio.get_event_loop()
    loop.run_until_complete(generate_token())
    print('ddd')
    '''

    #s.__authenticate()
    #print(s.upsert('Tasks', {'name': "A new task"}))
    #print(s.upsert_with_retries('Tasks', {'id':'b3dc7a68-a38f-11e9-b7ee-06684e9a08fe', 'name': "A new task"}))