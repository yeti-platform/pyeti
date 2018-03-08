
"""Wrapper around yeti CLI utilities."""
import argparse

from pyeti.scripts import addfiles
from pyeti.scripts import getfile
from pyeti import api

def fetch_endpoint():
    return "http://localhost:5000/api", None


def main():

    endpoint, apikey = fetch_endpoint()
    yeti_api = api.YetiApi(endpoint)

    parser = argparse.ArgumentParser()
    parser.add_argument('--json', '-j', action="store_true", help="Output raw JSON data when available.")
    subparsers = parser.add_subparsers(
        title=u'Available scripts',
        description=u'Available Yeti scripts',
        help=u'Script help')

    # File upload
    subparser = subparsers.add_parser("addfiles", description="Add files to Yeti.")
    subparser.add_argument("path", type=str, help="Path to files to upload.")
    subparser.add_argument("--tags", type=str, help="Comma-separated tags", default=[])
    subparser.add_argument(
        "--recurse", action="store_true", help="Recurse a directory", default=False)
    subparser.set_defaults(command="addfiles")

    # File info
    subparser = subparsers.add_parser("getfile", description="Fetch files from Yeti.")
    subparser.add_argument("hash", type=str, help="Path to files to upload.")
    subparser.add_argument("--save", type=str, help="Filename to dump file into.")
    subparser.set_defaults(command="getfile")

    # Eventually add other commands here...

    args = parser.parse_args()

    if args.command == "addfiles":
        addfiles.run(yeti_api, args)
    if args.command == "getfile":
        getfile.run(yeti_api, args)

if __name__ == '__main__':
    main()
