import glob
import json
import apt_pkg

from jinja2 import Template 
import sys

apt_pkg.init()

args = sys.argv[1:]
pre_release = False


def print_help():
    print(f"usage: python {sys.argv[0]} <tag> [-p|--pre-release]")
    print( "    -p, --pre-release: use this flag to indicate that the tag is a pre-release, and that the following json array of strings is the related files")
    exit(1)

if len(args) < 1:
    print_help()

for a in args:
    if a == "-p" or a == "--pre-release":
        pre_release = True

alpha_packages = []
latest_packages = []

with open('Packages', 'r') as f:
    packages = apt_pkg.TagFile(f)
    for pkg in packages:
        package = { 
            "name": pkg['Package'] ,
            "version": pkg['Version'],
            "description": pkg['Description'],
            "architecture": pkg['Architecture'],
            "file": pkg['Filename'],
            "debfile": pkg['Filename'][2:-5]
        }

        if pkg['Package'].endswith('alpha'):
            alpha_packages.append(package)
        else:
            latest_packages.append(package)

    all_packages = latest_packages + alpha_packages

    with open('index.html', 'w') as f_index:
        template = Template(open('templates/index_template', 'r').read())
        f_index.write(template.render(
            pre_release=pre_release,
            all_packages=all_packages,
            latest_packages=latest_packages,
            alpha_packages=alpha_packages
        ))

    with open('README.md', 'w') as f_md:
        template = Template(open('templates/README_template', 'r').read())
        f_md.write(template.render(
            pre_release=pre_release,
            all_packages=all_packages,
            latest_packages=latest_packages,
            alpha_packages=alpha_packages
        ))
