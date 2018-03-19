#!/usr/bin/env python
"""Fetches information on a file in Yeti."""
from timesketch_api_client import client

def fetch_indicators(yeti_api, entity):
    """Fetches Yeti indicators associated to a given entity."""
    indicators = yeti_api.related_indicators(entity)
    for i in indicators:
        print i['name']

def build_timesketch_query_string(indicator):
    """Builds a timesketch query out of a Yeti indicator."""
    if 'filesystem' in indicator['location']:
        fs_query = 'data_type:*fs* AND filename:"{0:s}"'
        return fs_query.format(indicator['pattern'])

    if 'history' in indicator['location']:
        history_query = 'data_type:*history* AND url:"{0:s}"'
        return history_query.format(indicator['pattern'])

def run(yeti_api, arguments):
    """Fetches information on a file in Yeti."""

    if not (arguments.id or arguments.name):
        print "Please specify at least an entity --id or --name."
        exit(-1)

    if arguments.id:
        entity = yeti_api.entity_get(arguments.id)
    else:
        entities = yeti_api.entity_search(name=arguments.name)
        if len(entities) != 1:
            print "More than one entity matches your query:"
            for e in entities:
                print "  {0:s}: {1:<30s}".format(e['name'], e['id'])
            print "Rerun the command specifing an --id parameter."
            exit(-1)
        entity = entities[0]

    indicators = yeti_api.related_indicators(entity)['data']
    print "Found {0:d} indicators for entity {1:s} ({2:s})".format(
        len(indicators), entity['name'], entity['id'])
    for i in indicators:
        print " Name: {0:s}, Pattern: {1:s}".format(
            i['name'], repr(i['pattern']))

    c = client.TimesketchApi(
        arguments.endpoint, arguments.username, arguments.password)
    sketch = c.get_sketch(arguments.sketch_id)
    for i in indicators:
        query_string = build_timesketch_query_string(i)
        response = sketch.explore(query_string=query_string)
        events = response['objects']
        if events:
            print "[!] Found {0:d} matching events for {1:s}".format(
                len(events), i['name'])
            for e in events:
                timestamp = e['_source']['datetime']
                description = e['_source']['timestamp_desc']
                message = e['_source']['message']
                labels = e['_source']['label']
                print "{0:s} {1:<30s} {2:s} {3:s}".format(
                    timestamp, description, message, labels)
            if arguments.tag:
                sketch.label_events(events, "yeti")
