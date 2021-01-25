# pyeti-python
Pyeti-Python (pyeti) is the bundle use to interface with the YETI API. This is the new package that can be installed directly with pip.
Pyeti-python allows you to extract data from YETI such as specific observables (malware, IP, domains ...). It can be used to plug in your own tool and enrich your Threat Intelligence feed with Yeti.

## Getting Started
To install it you can clone the repo and run the following command:

```
$ python3 setup.py install
```

You can also install it with pip:
```
$ pip3 install pyeti-python
``` 

Once installed the first thing to do is to get your API key from the Yeti interface.
[YETI API](yeti_api.png)

Then you can configure your script with the following information to test the connection:
```python
server="<IPofYETI>"
key="<APIKEY>"
tag="<NameoftheObservable>" # example: 'lokibot'

api = pyeti.YetiApi("http://%s:5000/api/" % server, api_key=key)
request = api.observable_search(tags=tag, count=50)
```

## Testing

You can run tests from the root directory by running:

    $ pip3 install nose
    $ python3 setup.py test
    
**Note that most tests require a full running install of Yeti on localhost:5000**

## Use cases

First thing is to import the library and instantiate a client.

```python
import pyeti, json    # json is only used for pretty printing in the examples below 
api = pyetix.YetiApi("http://localhost:5000/api/")
```

If you are using a self signed cert on your yeti instance you can set the `verify_ssl` parameter to `True` to ignore warnings.
Otherwise all ssl connections are verified by default.

```python
import pyeti, json    # json is only used for pretty printing in the examples below 
api = pyeti.YetiApi("http://localhost:5000/api/", verify_ssl=False)
```


### Adding observables

```python
results = api.observable_add("google.com", ['google'])
print(json.dumps(results, indent=4, sort_keys=True))
```
### Bulk add

```python
results = api.observable_bulk_add(["google.com", "bing.com", "yahoo.com"])
print(len(results))
3
print(json.dumps(results[1], indent=4, sort_keys=True))
```

### Get a single observable

```python
results = api.observable_add("google.com")
print(results['id'])
info = api.observable_details(results['id'])
print(json.dumps(info, indent=4, sort_keys=True))
```

### Search for observables

```python
api.observable_add("search-domain.com")
result = api.observable_search(value="search-dom[a-z]+", regex=True)
print(json.dumps(result, indent=4, sort_keys=True))
```

### Add observables
```python
result = api.observable_file_add("/tmp/hello.txt", tags=['benign'])
print(json.dumps(result, indent=4, sort_keys=True))
# Get file contents
api.observable_file_contents(objectid="594fff86bf365e6270f8914b")
'Hello!\n'
api.observable_file_contents(filehash="e134ced312b3511d88943d57ccd70c83") # you can also use any hash computed above
'Hello!\n'
```
#License
This project is licensed under the Apache License - see the LICENSE.md file for details
