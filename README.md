# pyeti
Python bindings for Yeti's API

## Installation

`$ python setup.py install` should get you started. After this gets a little more maturity, we will submit it to Pypy for usage with `pip`.

## Testing

You can run tests from the root directory by running:

    $ pip install nose
    $ python setup.py test
    
**Note that most tests require a full running install of Yeti on localhost:5000**

## Some examples

First thing is to import the library and instantiate a client.

```python
import pyeti, json    # json is only used for pretty printing in the examples below 
api = pyeti.YetiApi("http://localhost:5000/api/")
```

### Adding observables

```python
results = api.observable_add("google.com", ['google'])
print(json.dumps(results, indent=4, sort_keys=True))
{
    "context": [],
    "created": "2017-06-25T17:33:51.735000",
    "description": null,
    "human_url": "http://localhost:5000/observable/594ff3ffbf365e53fbae38c9",
    "id": "594ff3ffbf365e53fbae38c9",
    "last_analyses": {},
    "sources": [
        "API"
    ],
    "tags": [
        {
            "first_seen": "2017-06-25T17:33:51.746000",
            "fresh": true,
            "last_seen": "2017-06-25T17:33:51.746000",
            "name": "google"
        }
    ],
    "type": "Hostname",
    "url": "http://localhost:5000/api/observable/594ff3ffbf365e53fbae38c9",
    "value": "google.com"
}
```

### Bulk add

```python
results = api.observable_bulk_add(["google.com", "bing.com", "yahoo.com"])
print(len(results))
3
print(json.dumps(results[1], indent=4, sort_keys=True))
{
    "context": [],
    "created": "2017-06-25T17:39:31.051000",
    "description": null,
    "human_url": "http://localhost:5000/observable/594ff553bf365e53fbae38cc",
    "id": "594ff553bf365e53fbae38cc",
    "last_analyses": {},
    "sources": [
        "API"
    ],
    "tags": [],
    "type": "Hostname",
    "url": "http://localhost:5000/api/observable/594ff553bf365e53fbae38cc",
    "value": "bing.com"
}
```

### Get a single observable

```python
results = api.observable_add("google.com")
print(results['id'])
info = api.observable_details(results['id'])
print(json.dumps(info, indent=4, sort_keys=True))
{
    "context": [],
    "created": "2017-06-25T17:33:51.735000",
    "description": null,
    "human_url": "http://localhost:5000/observable/594ff3ffbf365e53fbae38c9",
    "id": "594ff3ffbf365e53fbae38c9",
    "last_analyses": {},
    "sources": [
        "API"
    ],
    "tags": [
        {
            "first_seen": "2017-06-25T17:33:51.746000",
            "fresh": true,
            "last_seen": "2017-06-25T17:33:51.746000",
            "name": "google"
        }
    ],
    "type": "Hostname",
    "url": "http://localhost:5000/api/observable/594ff3ffbf365e53fbae38c9",
    "value": "google.com"
}
```

### Search for observables

```python
api.observable_add("search-domain.com")
result = api.observable_search(value="search-dom[a-z]+")
print(json.dumps(result, indent=4, sort_keys=True))
[
    {
        "context": [],
        "created": "2017-06-25T17:57:28.994000",
        "description": null,
        "human_url": "http://localhost:5000/observable/594ff988bf365e58c4c2b8ef",
        "id": "594ff988bf365e58c4c2b8ef",
        "last_analyses": {},
        "sources": [
            "API"
        ],
        "tags": [],
        "type": "Hostname",
        "url": "http://localhost:5000/api/observable/594ff988bf365e58c4c2b8ef",
        "value": "search-domain.com"
    }
]

```

### Add files

```python
result = api.observable_file_add("/tmp/hello.txt", tags=['benign'])
print(json.dumps(result, indent=4, sort_keys=True))
[
    {
        "context": [],
        "created": "2017-06-25T18:23:02.471000",
        "description": null,
        "hashes": [
            {
                "hash": "sha256",
                "value": "b22b009134622b6508d756f1062455d71a7026594eacb0badf81f4f677929ebe"
            },
            {
                "hash": "sha512",
                "value": "eb22d991d6d86641d95e01a804025fc210491286a30f3114dd1469c7457c03e807506f5615bc9065f47a6ee2208364f643837f2298738b4f5c53797124f41f60"
            },
            {
                "hash": "md5",
                "value": "e134ced312b3511d88943d57ccd70c83"
            },
            {
                "hash": "sha1",
                "value": "a8d191538209e335154750d2df575b9ddfb16fc7"
            }
        ],
        "human_url": "http://localhost:5000/observable/594fff86bf365e6270f8914b",
        "id": "594fff86bf365e6270f8914b",
        "last_analyses": {},
        "mime_type": "text/plain",
        "sources": [],
        "tags": [
            {
                "first_seen": "2017-06-25T18:23:02.544000",
                "fresh": true,
                "last_seen": "2017-06-25T18:23:02.544000",
                "name": "benign"
            }
        ],
        "type": "File",
        "url": "http://localhost:5000/api/observable/594fff86bf365e6270f8914b",
        "value": "FILE:b22b009134622b6508d756f1062455d71a7026594eacb0badf81f4f677929ebe"
    }
]
# Get file contents
api.observable_file_contents(id="594fff86bf365e6270f8914b")
'Hello!\n'
api.observable_file_contents(hash="e134ced312b3511d88943d57ccd70c83") # you can also use any hash computed above
'Hello!\n'
```


