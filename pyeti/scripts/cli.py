
"""Wrapper around yeti CLI utilities."""
import argparse

from pyeti.scripts import upload
from pyeti import api

def fetch_endpoint():
    return "http://localhost:5000/api", None


def main():

    endpoint, apikey = fetch_endpoint()
    yeti_api = api.YetiApi(endpoint)

    parser = argparse.ArgumentParser()
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
    subparser.set_defaults(command="upload")

    # File info
    subparser = subparsers.add_parser("getfiles", description="Fetch files from Yeti.")
    subparser.add_argument("hash", type=str, help="Path to files to upload.")
    subparser.add_argument("--download", action="store_true", help="Comma-separated tags", default=False)
    subparser.set_defaults(command="getfiles")

    # Eventually add other commands here...

    args = parser.parse_args()

    if args.command == "upload":
        upload.run(yeti_api, args)

if __name__ == '__main__':
    main()
