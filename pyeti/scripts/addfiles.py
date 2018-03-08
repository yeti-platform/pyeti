#!/usr/bin/env python
"""Uploads a series of files to Yeti."""

import glob
import json
import os
import sys
from tqdm import tqdm


def run(yeti_api, arguments):
    """Uploads a series of files to Yeti."""
    paths = []

    initial_path = os.path.abspath(arguments.path)

    if arguments.recurse:
        for dirpath, _, filenames in os.walk(initial_path):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                if os.path.isdir(path):
                    sys.stderr.write("{} is a directory. Skipping\n".format(path))
                    continue
                paths.append(path)
    else:
        for path in glob.iglob(initial_path):
            if os.path.isdir(path):
                sys.stderr.write("{} is a directory. Skipping\n".format(path))
                continue
            paths.append(path)

    if not paths:
        sys.stderr.write("Please provide a file to upload.\n")
        exit()

    if len(paths) > 2:
        for path in paths:
            sys.stderr.write(path)
        sys.stderr.write(
            "You are about to upload {} files from '{}' to Yeti. "
            "Proceed? [Y/n] ".format(
                len(paths),
                initial_path))
        sys.stderr.flush()
        choice = raw_input().lower()
        if choice and choice not in ["Y", "y"]:
            sys.stderr.write("Bailing.\n")
            exit()

    tags = arguments.tags
    if tags:
        tags = tags.split(',')

    results = []
    for path in tqdm(paths, desc="Uploading files"):
        results.extend(yeti_api.observable_file_add(path, tags=tags))

    if arguments.json:
        sys.stdout.write(json.dumps(results, indent=4, sort_keys=True))
        sys.stdout.flush()
    else:
        sys.stdout.write("{:<70} {:<20} {:<20}\n".format("SHA256", "Tags", "Filenames"))
        sys.stdout.flush()
        for result in results:
            sys.stdout.write("{:<70} {:<20} {:<20}\n".format(
                [h['value'] for h in result['hashes'] if h['hash'] == "sha256"][0],
                ", ".join([t['name'] for t in result['tags']]),
                ", ".join(result['filenames'])))
        sys.stdout.write("Succesfully uploaded {} file{}.\n".format(
            len(results),
            "s" if len(results) > 1 else ""))
        sys.stdout.flush()
