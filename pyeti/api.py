import datetime
import requests
import validators
from enum import Enum


class endpoints(tuple, Enum):
    observable = ("/api/v2/observables/{}", "GET")
    observable_new = ("/api/v2/observables", "POST")
    observable_search = ("/api/v2/observables/search", "POST")
    observable_text = ("/api/v2/observables/add_text", "POST")
    entity = ("/api/v2/entities/{}", "GET")
    entity_new = ("/api/v2/entities", "POST")
    entity_search = ("/api/v2/entities/search", "POST")
    entity_patch = ("/api/v2/entities/{}", "PATCH")
    entities = ("/api/v2/entities", "GET")


class ObservableType(str, Enum):
    ip = "ip"
    hostname = "hostname"
    url = "url"
    observable = "observable"
    guess = "guess"
    email = "email"
    file = "file"
    sha256 = "sha256"
    sha1 = "sha1"
    md5 = "md5"
    asn = "asn"
    cidr = "cidr"
    certificate = "certificate"
    bitcoin_wallet = "bitcoin_wallet"
    path = "path"
    mac_address = "mac_address"
    command_line = "command_line"
    registry_key = "registry_key"
    imphash = "imphash"
    tlsh = "tlsh"
    ssdeep = "ssdeep"


class EntityType(str, Enum):
    threat_actor = "threat-actor"
    intrusion_set = "intrusion-set"
    tool = "tool"
    malware = "malware"
    campaign = "campaign"
    attack_pattern = "attack-pattern"
    identity = "identity"
    exploit = "exploit"


class YetiClient:
    def __init__(self, api_key, base_url="http://localhost:8000") -> None:
        self.base_url = base_url
        self.headers = {"x-yeti-apikey": api_key}

    def __make_requests(self, method: str, endpoint: str, **kwargs):
        url = self.__get_url(endpoint)
        return requests.request(method, url, headers=self.headers, **kwargs).json()

    def __get_url(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        if validators.url(url):
            return url
        raise ValueError(f"Invalid URL: {url}")

    def __add_observable(self, value: str, observable_type: str, tags: list = None):
        endpoint = endpoints.observable_new.value[0]
        method = endpoints.observable_new.value[1]
        data = {"type": observable_type, "value": value}
        return self.__make_requests(method, endpoint, json=data)

    def __add_entity(
        self, value: str, entity_type: str, tags: list = None, aliases: list = None
    ):
        endpoint = endpoints.entity_new.value[0]
        method = endpoints.entity_new.value[1]

        data = {
            "entity": {
                "root_type": "entity",
                "id": "string",
                "type": entity_type,
                "name": value,
                "description": "",
                "created": datetime.datetime.now(),
                "modified": datetime.datetime.now(),
                "relevant_tags": tags,
                "aliases": [],
            }
        }
        return self.__make_requests(method, endpoint, json=data)

    def add_ipadress(self, ipadress: str, tags: list = None):
        return self.__add_observable(ipadress, ObservableType.ip, tags)

    def add_hostname(self, hostname: str, tags: list = None):
        return self.__add_observable(hostname, ObservableType.hostname, tags)

    def add_url(self, url: str, tags: list = None):
        return self.__add_observable(url, ObservableType.url, tags)

    def add_email(self, email: str, tags: list = None):
        return self.__add_observable(email, ObservableType.email, tags)

    def add_file(self, file: str, tags: list = None):
        return self.__add_observable(file, ObservableType.file, tags)

    def add_path(self, path: str, tags: list = None):
        return self.__add_observable(path, ObservableType.path, tags)

    def add_asn(self, asn: str, tags: list = None):
        return self.__add_observable(asn, ObservableType.asn, tags)

    def add_cidr(self, cidr: str, tags: list = None):
        return self.__add_observable(cidr, ObservableType.cidr, tags)

    def add_certificate(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.certificate, tags)

    def add_bitcoin_wallet(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.bitcoin_wallet, tags)

    def add_path(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.path, tags)

    def add_macaddress(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.mac_address, tags)

    def add_command_line(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.command_line, tags)

    def add_registry_key(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.registry_key, tags)

    def add_imphash(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.imphash, tags)

    def add_tlsh(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.tlsh, tags)

    def add_ssdeep(self, value: str, tags: list = None):
        return self.__add_observable(value, ObservableType.ssdeep, tags)

    def add_text(self, value: str, tags: list = None):
        data = {"text": value, "tags": tags}
        endpoint = endpoints.observable_text.value[0]
        method = endpoints.observable_text.value[1]
        return self.__make_requests(method, endpoint, json=data)

    def observable_search(
        self, value: str, observable_type: str, tags: list = None, count=50, page=0
    ):
        endpoint = endpoints.observable_search.value[0]
        method = endpoints.observable_search.value[1]
        data = {"type": observable_type, "value": value, "count": count, "page": page}
        return self.__make_requests(method, endpoint, json=data)

    def observable(self, observable_id: str):
        endpoint = endpoints.observable.value[0]
        method = endpoints.observable.value[1]
        return self.__make_requests(method, endpoint.format(observable_id))

    def add_thread_actor(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.threat_actor, tags)

    def add_intrusion_set(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.intrusion_set, tags)

    def add_tool(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.tool, tags)

    def add_malware(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.malware, tags)

    def add_campaign(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.campaign, tags)

    def add_attack_pattern(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.attack_pattern, tags)

    def add_identity(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.identity, tags)

    def add_exploit(self, value: str, tags: list = None):
        return self.__add_entity(value, EntityType.exploit, tags)

    def entity(self, entity_id: str):
        endpoint = endpoints.entity.value[0]
        method = endpoints.entity.value[1]
        return self.__make_requests(method, endpoint.format(entity_id))

    def entity_search(
        self, value: str, entity_type: str, tags: list = None, count=50, page=0
    ):
        endpoint = endpoints.entity_search.value[0]
        method = endpoints.entity_search.value[1]
        data = {"type": entity_type, "value": value, "count": count, "page": page}
        return self.__make_requests(method, endpoint, json=data)

    def entity_patch(self, entity_id: str, type:str=None, name:str=None ,tags: list = None, aliases: list = None):
        endpoint = endpoints.entity_patch.value[0]
        method = endpoints.entity_patch.value[1]
        entity = self.entity(entity_id)
        entity['modified'] = datetime.datetime.now()
        if type:
            entity['type'] = type
        if name:
            entity['name'] = name
        if tags:
            entity['relevant_tags'] = tags

        if aliases:
            entity['aliases'] = aliases
        data = {"entity": entity}
        return self.__make_requests(method, endpoint.format(entity_id), json=data)
    
    def entities(self):
        endpoint = endpoints.entities.value[0]
        method = endpoints.entities.value[1]
        return self.__make_requests(method, endpoint)

