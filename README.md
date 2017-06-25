# pyeti
Python bindings for Yeti's API

## Installation

`$ python setup.py install` should get you started.

## Some examples

First thing is to import the library and instantiate a client.

```
import pyeti
api = pyeti.YetiApi("http://localhost:5000/api/")
```

*Adding observables*

```python
results = api.observable_add("google.com", ['google'])
import json
print json.dumps(results, indent=4, sort_keys=True)
```

```json
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
