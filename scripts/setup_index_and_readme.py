import glob
import json
from string import Template

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

pre_release_files = []

if pre_release :
    pre_release_files = json.loads(pre_release_files_json) 


index_mappings = { "tag": args[0], "latest_packages": "", "all_packages": "", "unstable_packages": "" }
readme_mappings = { "latest_packages": "", "pre_release_packages": "" }

if pre_release:
    readme_mappings["pre_release_packages"] = """
## Pre-release/unstable packages ⚠️

> [!IMPORTANT]
> The following packages are unstable and thus not recommended.
"""

packages = open("Packages").read().split("\n\n")
packages.pop()

for package in packages:
    package = package.split("\n")
    package = { p.split(": ")[0]: p.split(": ")[1] for p in package }

    print(package)

    html     = f"<li><a href=\"{package['Filename']}\">{package['Package']}</a><br>Version: {package['Version']}<br>Description: {package['Description']}<br>Filename: <a href=\"{package['Filename']}\">{package['Filename'][2:-5]}</a></li>\n"
    markdown = f"- {package['Package']} - [{package['Filename'][2:-5]}](https://ppa.gama-platform.org/{package['Filename'][2:]})\n"

    if pre_release and ( package["Filename"] in pre_release_files or package["Package"].endswith("unstable")):
        index_mappings["unstable_packages"]     += html
        readme_mappings["pre_release_packages"] += markdown
    else:
        index_mappings["latest_packages"]  += html
        readme_mappings["latest_packages"] += markdown
        index_mappings["tag"] = package["Version"]
    

files = glob.glob("*.deb.html")

for file in files:
    index_mappings["all_packages"] += f"<div class=\"file-list-item\"><a href=\"/{file}\">{file[:-5]}</a><br></div>\n"

template_index = Template(open("templates/index_template").read())
template_index = template_index.substitute(**index_mappings)
f = open("index.html", "w")
f.write(template_index)


template_readme   = Template(open("templates/README_template").read())
template_readme   = template_readme.substitute(**readme_mappings)
f = open("README.md", "w")
f.write(template_readme)