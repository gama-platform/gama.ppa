import glob
import json

import sys

args = sys.argv[1:]
pre_release = False
pre_release_files_json = None

def print_help():
    print(f"usage: python {sys.argv[0]} <tag> [-p|--pre-release <files_expresed_as_a_json_array_of_str>]")
    print( "    -p, --pre-release: use this flag to indicate that the tag is a pre-release, and that the following json array of strings is the related files")
    exit(1)


if len(args) < 1:
    print_help()

for a in args:
    if a == "-p" or a == "--pre-release":
        pre_release = True
    elif pre_release:
        pre_release_files_json = a

if pre_release and not pre_release_files_json:
    print_help()

