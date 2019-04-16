#!/usr/bin/env python
"""Fetches information on a file in Yeti."""
import sys
import json

def run(yeti_api, arguments):

    """Fetches information on a file in Yeti."""
    filehash = arguments.hash
    results = yeti_api.observable_search(hashes__value=filehash)
    if not results:
        sys.stderr.write("{} was not found in the database.\n".format(filehash))
        sys.stderr.flush()
        exit(-1)

    fileinfo = results[0]
    if arguments.json:
        sys.stdout.write(json.dumps(results, indent=4, sort_keys=True))
        sys.stdout.flush()
    else:
        tag_names = [t["name"] for t in fileinfo["tags"]]
        print("File info:")
        print("{:>15}   {}".format("Added on:", fileinfo["created"]))
        print("{:>15}   {}".format("Filenames:", ", ".join(fileinfo["filenames"])))
        print("{:>15}   {}".format("Tags:", ", ".join(tag_names)))
        print("{:>15}   {}".format("MIME-type:", fileinfo["mime_type"]))
        print("{:>15}   {}".format("URL:", fileinfo["human_url"]))
        print("\nHashes:")
        for h in fileinfo['hashes']:
            print("{:>15}   {}".format(h['hash']+":", h['value']))

    if arguments.save:
        with open(arguments.save, 'wb') as dumpfile:
            dumpfile.write(yeti_api.observable_file_contents(objectid=fileinfo['id']))
        sys.stderr.write("\nDumped file to {}\n".format(arguments.save))
        sys.stderr.flush()
