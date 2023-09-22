import glob
from string import Template

import sys

args = sys.argv[1:]

if (len(args) < 1):
    print(f"usage: python {sys.argv[0]} <tag>")
    exit(1)

index_mappings = { "tag": args[0], "latest_packages": "", "all_packages": "" }

readme_list = ""

packages = open("Packages").read().split("\n\n")
packages.pop()

for package in packages:
    package = package.split("\n")
    package = { p.split(": ")[0]: p.split(": ")[1] for p in package }

    print(package)

    index_mappings["latest_packages"] += f"<li><a href=\"{package['Filename']}\">{package['Package']}</a><br>Version: {package['Version']}<br>Description: {package['Description']}<br>Filename: <a href=\"{package['Filename']}\">{package['Filename'][2:-5]}</a></li>\n"
    readme_list += f"- {package['Package']} - [{package['Filename'][2:-5]}](https://ppa.gama-platform.org/{package['Filename'][2:]})\n"

files = glob.glob("*.deb.html")

for file in files:
    index_mappings["all_packages"] += f"<div class=\"file-list-item\"><a href=\"/{file}\">{file[:-5]}</a><br></div>\n"

template_index = Template(open("templates/index_template").read())
template_index = template_index.substitute(**index_mappings)
f = open("index.html", "w")
f.write(template_index)


template_readme   = Template(open("templates/README_template").read())
template_readme   = template_readme.substitute(latest_packages=readme_list)
f = open("README.md", "w")
f.write(template_readme)