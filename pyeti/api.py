#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python interface to the Yeti REST API."""

import logging
import os

import requests


class YetiApi(object):
    """Python interface to the Yeti REST API."""

    def __init__(self, url, auth=tuple(), api_key=None):
        super(YetiApi, self).__init__()
        if not url.endswith('/'):
            url += "/"
        self.yeti_url = url
        self.auth = auth
        self.api_key = api_key
        self._test_connection()

    def entity_search(self, count=50, offset=1, regex=False, **kwargs):
        """Fetches a list of indicators associated with an Entity.

        Args:
            count: How many Entities you want to fetch.
            offset: How many sets of *count* Entities you want to skip
                    (total skipped = offset * count)
            regex: Use regular expressions to Search.
            kwargs: Remaining keyword arguments will be transformed in a JSON
                    object that will act as the filter.

        Returns:
          A list of indicators.
        """
        json = {
            "filter": kwargs,
            "params": {
                "page": offset,
                "range": count,
                "regex": regex
            }
        }
        return self._make_post("entitysearch/", json=json)

    def entity_get(self, objectid):
        """Fetches an entity by ID.

        Returns:
           JSON representation of the requested Entity."""
        return self._make_get("entity/{}".format(objectid))

    def related_indicators(self, entity, **kwargs):
        """Fetches indicators linked to a given entity.

        Args:
           entity: JSON dict representing the Entity to search indicators for.
           kwargs: Remaining keyword arguments will be transformed in a JSON
                   object that will act as the filter.

        Returns:
           A list of matching JSON Indicators.
        """
        url = "neighbors/tuples/{0:s}/{1:s}/indicator".format(
            entity['type'], entity['id'])
        json = {"filter": kwargs}
        return self._make_post(url, json=json)

    def analysis_match(self, observables):
        """Matches a list of observables against Yeti indicators.

        Args:
            observables: An array of strings representing observables

        Returns:
            JSON representation of match response.
        """
        json = {"observables": observables}
        return self._make_post("analysis/match", json=json)

    def observable_search(self, count=50, offset=1, regex=False, **kwargs):
        """Search for observables.

        Args:
            count: How many Observables you want to fetch.
            offset: How many sets of *count* Observables you want to skip
                    (total skipped = offset * count)
            regex: Use regular expressions to Search.
            kwargs: Remaining keyword arguments will be transformed in a JSON
                    object that will act as the filter.

        Returns:
            Array of JSON representations of matching Observables.
        """
        json = {"filter": kwargs, "params": {"page": offset, "range": count, "regex": regex}}
        return self._make_post("observablesearch/", json=json)

    def observable_details(self, objectid):
        """Get details on an Observable.
        Args:
            objectid: A string representing the observable's ObjectID

        Returns:
            JSON representation of the requested Observable.
        """
        return self._make_get("observable/{}".format(objectid))

    def observable_add(self, value, tags=None, context=None, source="API"):
        """Add an observable to the dataset

        Args:
            value: the Observable value
            tags: An array of strings representing tags
            context: A dictionary object with context information
            source: A string representing the source of the data. Defaults to
                    "API".

        Returns:
            JSON representation of the created observable.
        """
        if tags is None:
            tags = []
        if context is None:
            context = {}
        json = {
            "tags": tags,
            "value": value,
            "source": source,
            "context": context
        }
        return self._make_post('observable/', json=json)

    def observable_change(self, objectid, tags=None, context=None):
        """Add tags to an observable.

        Args:
            objectid: The observable's ObjectID
            tags: Tags to add
            context: Context to add

        Returns:
            JSON representation of the updated observable
        """
        if tags is None:
            tags = []
        if context is None:
            context = {}
        json = {"id": objectid, "tags": tags, "context": context}
        result = self._make_post('observable/', json=json)
        return result

    def observable_delete(self, objectid):
        """Deletes an observable.

        Args:
            objectid: The observable's ObjectID

        Returns:
            Operation status in JSON.
        """
        self._make_delete('observable/{}'.format(objectid))
        return {'status': 'deleted', 'id': objectid}

    def observable_file_add(self, path, tags=None, context=None):
        """Upload a file to the dataset

        Args:
            path: The path to the file
            tags: An array of strings representing tags
            context: A dictionary object with context information
            source: A string representing the source of the data. Defaults to
                    "API".

        Returns:
            JSON representation of the created observable.
        """
        if tags is None:
            tags = []
        if context is None:
            context = {}
        path = os.path.realpath(os.path.normpath(os.path.expanduser(path)))
        filename = os.path.basename(path)
        files = {'files': (filename, open(path, 'rb'))}
        fileinfos = self._make_post(
            'file/addfile',
            files=files
        )
        if not (tags or context):
            return fileinfos

        updated_fileinfo = []
        for info in fileinfos:
            info = self.observable_change(info['id'], tags, context)
            updated_fileinfo.append(info)

        return updated_fileinfo

    def observable_file_contents(self, objectid=None, filehash=None):
        """Fetches the content of a File observable.
        Args:
            objectid: The observable's ObjectID.
            filehash: The observable's hash.

        Returns:
            Binary data containing the file's contents.
        """
        if objectid is not None:
            return self._make_get('file/get/id/{}'.format(objectid))
        elif filehash is not None:
            return self._make_get('file/get/hash/{}'.format(filehash))
        else:
            raise ValueError("You need to pass an id or hash parameter.")

    def observable_bulk_add(self, observables, tags=None):
        """Add an observable to the dataset

        Args:
            value: the Observable value
            tags: An array of strings representing tags
            context: A dictionary object with context information
            source: A string representing the source of the data. Defaults to
                    "API".

        Returns:
            JSON representation of the created observable.
        """
        if tags is None:
            tags = []
        json = {"observables": [{"tags": tags, "value": o} for o in observables]}
        return self._make_post('observable/bulk', json=json)

    def analytics_oneshot_run(self, name_of_oneshot, value, type_obversable):

        oneshot = []

        result = {}

        all_analytics = self.analytics_oneshot_list()

        if all_analytics:
            oneshot = [item for item in all_analytics
                       if item['name'] == name_of_oneshot]

        if oneshot:
            if type_obversable in oneshot[0]['acts_on']:

                observable = self.observable_add(value)

                if observable:
                    oneshot_inst = self._make_post('analytics/oneshot/%s/run' % oneshot[0]['id'],
                                                   data={'id': observable['id']})
                    status = self.analytics_oneshot_status(oneshot_inst['_id'])
                    if status:
                        while status['status'] == 'running':
                            status = self.analytics_oneshot_status(oneshot_inst['_id'])
                            continue

                        if status['status'] == 'finished':
                            result = status['results']
                            return result
                        else:
                            logging.error('Error Oneshot Processing %s with %s' % (name_of_oneshot, value))
        return result

    def analytics_oneshot_status(self, id_oneshot):

        status = {}

        if id_oneshot:
            r = self._make_get('analytics/oneshot/%s/status' % id_oneshot)

            if r:
                status = r
                return status
            else:
                logging.error('Error to check status %s' % id_oneshot)
        else:
            logging.error('id_oneshot is empty %s' % id_oneshot)

        return status

    def analytics_oneshot_list(self):
        list_analytics = []

        r = self._make_get('analytics/oneshot')

        if r:
            list_analytics = r
            return list_analytics
        else:
            logging.error('Error to list oneshot analytics %s' % self.yeti_url + 'analytics/oneshot')

        return list_analytics

    def _test_connection(self):
        if self._make_post("observablesearch/"):  # replace this with a more meaningful URL
            logging.debug("Connection to %s successful", self.yeti_url)
        else:
            logging.debug("Conncetion to %s failed", self.yeti_url)

    def _make_post(self, url, **kwargs):
        return self._make_request(url, method="POST", **kwargs)

    def _make_get(self, url):
        return self._make_request(url)

    def _make_delete(self, url):
        return self._make_request(url, method="DELETE")

    def _make_request(self, url, **kwargs):
        url = "{}{}".format(self.yeti_url, url)

        method = kwargs.pop("method", "GET")

        headers = {'Accept': 'application/json'}
        if self.api_key:
            headers.update({"X-Api-Key": self.api_key})

        if method == "POST":
            resp = requests.post(url, headers=headers, auth=self.auth, **kwargs)
        if method == "GET":
            resp = requests.get(url, auth=self.auth, headers=headers)
        if method == "DELETE":
            resp = requests.delete(url, auth=self.auth, headers=headers)

        if resp.status_code == 200:
            logging.debug("Success (%s)", resp.status_code)
            if "json" in resp.headers.get('content-type'):
                return resp.json()
            return resp.content
        else:
            logging.error("An error occurred (%s): %s", resp.status_code, url)


if __name__ == '__main__':
    pass
