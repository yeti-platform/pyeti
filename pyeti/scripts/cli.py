
"""Wrapper around yeti CLI utilities."""
import argparse

from pyeti.scripts import addfiles
from pyeti.scripts import getfile
#from pyeti.scripts import timesketch
from pyeti import api

def fetch_endpoint_config():
    """Loads and returns configuration data to connect to Yeti.

    Returns:
        An (endpoint, apikey) tuple used to initialize a YetiApi object.
    """
    return "http://localhost:5000/api", "c2ffb97aed9aea46dd973f45c549e1d9f569952d4bc3e4b67ed36dce1f60bccb7dbdb32d2d30b76e"


def main():

    endpoint, api_key = fetch_endpoint_config()
    yeti_api = api.YetiApi(endpoint, api_key=api_key)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--json', '-j', action="store_true",
        help="Output raw JSON data when available.")
    subparsers = parser.add_subparsers(
        title=u'Available scripts',
        description=u'Available Yeti scripts',
        help=u'Script help')

    # File upload
    subparser = subparsers.add_parser(
        "addfiles", description="Add files to Yeti.")
    subparser.add_argument("path", type=str, help="Path to files to upload.")
    subparser.add_argument(
        "--tags", type=str, help="Comma-separated tags", default=[])
    subparser.add_argument(
        "--recurse", action="store_true", help="Recurse a directory",
        default=False)
    subparser.set_defaults(command="addfiles")

    # File info
    subparser = subparsers.add_parser(
        "getfile", description="Fetch files from Yeti.")
    subparser.add_argument("hash", type=str, help="Path to files to upload.")
    subparser.add_argument(
        "--save", type=str, help="Filename to dump file into.")
    subparser.set_defaults(command="getfile")

    # Timesketch
    subparser = subparsers.add_parser(
        "timesketch", description="Interact with a Timesketch instance.")
    subparser.add_argument("endpoint", type=str, help="Timesketch URL")
    subparser.add_argument("username", type=str, help="Timesketch username")
    subparser.add_argument("password", type=str, help="Timesketch password")
    subparser.add_argument(
        "sketch_id", type=int, help="ID of the sketch to inspect.")
    subparser.add_argument(
        "--name", type=str, help="Entity name to fetch indicators from.")
    subparser.add_argument(
        "--id", type=str, help="Entity ID to fetch indicators from.")
    subparser.add_argument(
        "--tag", action="store_true",
        help="Matched events in Timesketch should be tagged.")
    subparser.set_defaults(command="timesketch")

    # Eventually add other commands here...

    args = parser.parse_args()

    if args.command == "addfiles":
        addfiles.run(yeti_api, args)
    if args.command == "getfile":
        getfile.run(yeti_api, args)
    #if args.command == "timesketch":
    #    timesketch.run(yeti_api, args)

if __name__ == '__main__':
    main()
