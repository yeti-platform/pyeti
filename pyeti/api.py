import requests
import validators
from enum import Enum

class endpoints(tuple,Enum):
    observable = ('/api/v2/observables/{}','GET')
    observable_new = ('/api/v2/observables','POST')
    observable_search = ('/api/v2/observables/search','POST')

class ObservableType(str, Enum):
    ip = 'ip'
    hostname = 'hostname'
    url = 'url'
    observable = 'observable'
    guess = 'guess'
    email = 'email'
    file = 'file'
    sha256 = 'sha256'
    sha1 = 'sha1'
    md5 = 'md5'
    asn = 'asn'
    cidr = 'cidr'
    certificate = 'certificate'
    bitcoin_wallet = 'bitcoin_wallet'
    path = 'path'
    mac_address = 'mac_address'

class YetiClient:
    
    def __init__(self,api_key,base_url='http://localhost:8000') -> None:
        self.base_url = base_url
        self.headers = {'x-yeti-apikey': api_key}
    
    def __make_requests(self,method:str,endpoint:str,**kwargs):
        url = self.__get_url(endpoint)
        return requests.request(method,url,headers=self.headers,**kwargs).json()

    
    def __get_url(self,endpoint:str):
        url = f'{self.base_url}{endpoint}'
        if validators.url(url):
            return url
        raise ValueError(f'Invalid URL: {url}')
    
    def __add_observable(self,value:str,observable_type:str,tags:list=None):
        endpoint = endpoints.observable_new.value[0]
        method = endpoints.observable_new.value[1]
        data = {'type':observable_type,'value':value}
        return self.__make_requests(method,endpoint,json=data)
    
    def add_ipadress(self,ipadress:str,tags:list=None):
        
        return self.__add_observable(ipadress,ObservableType.ip,tags) 
   
    def add_hostname(self,hostname:str,tags:list=None):
        return self.__add_observable(hostname,ObservableType.hostname,tags)

    def add_url(self,url:str,tags:list=None):
        return self.__add_observable(url,ObservableType.url,tags)
    
    def add_email(self,email:str,tags:list=None):
        return self.__add_observable(email,ObservableType.email,tags)
    
    def add_file(self,file:str,tags:list=None):
        return self.__add_observable(file,ObservableType.file,tags)

    def add_path(self,path:str,tags:list=None):
        return self.__add_observable(path,ObservableType.path,tags)
    
    def add_asn(self,asn:str,tags:list=None):
        return self.__add_observable(asn,ObservableType.asn,tags)

    def add_cidr(self,cidr:str,tags:list=None):
        return self.__add_observable(cidr,ObservableType.cidr,tags)
    
    def add_certificate(self,value:str,tags:list=None):
        return self.__add_observable(value,ObservableType.certificate,tags)
    
    def add_bitcoin_wallet(self,value:str,tags:list=None):
        return self.__add_observable(value,ObservableType.bitcoin_wallet,tags)

    def observable(self, observable_id:str):
        endpoint = endpoints.observable.value[0]
        method = endpoints.observable.value[1]
        return self.__make_requests(method,endpoint.format(observable_id))

    def observable_search(self,value:str,observable_type:str,tags:list=None,count=50,page=0):
        endpoint = endpoints.observable_search.value[0]
        method = endpoints.observable_search.value[1]
        data = {'type':observable_type,'value':value,'count':count,'page':page}
        return self.__make_requests(method,endpoint,json=data)