import glob
import sys
import os

from jinja2 import Template 

args = sys.argv[1:]

pre_release = False
p_flag_index = -1

for i, a in enumerate(args):
    if pre_release:
        pass
    if a == "-p" or a == "--pre-release":
        pre_release = True
        p_flag_index = i

if pre_release:
    args.pop(p_flag_index)


if (len(args) < 2):
    print(f"usage: python {sys.argv[0]} [-p|--pre-release] <repository> <tag>")
    print( "    -p, --pre-release: use this flag to indicate that the tag is a pre-release")
    exit(1)

files = glob.glob("*.deb")
repo = args[0]
tag = args[1]

for deb in files:
    with open("templates/package_template", "r") as f:
        template_deb_file = Template(f.read())
        with open(f"{deb}.html", "w") as fw:
            fw.write(template_deb_file.render(repo=repo, tag=tag, file=deb))

with open("templates/_header_template", "r") as f:
    template_header = Template(f.read())

    alpha_packages = []
    latest_package = []

    if pre_release:
        latest_package = [ d[:-5] for d in glob.glob("*.deb.html") ]
        alpha_packages = glob.glob("*.deb")
    else:
        latest_package = glob.glob("*.deb")
    

    with open("__site/_headers", "w") as fw:
        fw.write(template_header.render(
            latest_package=latest_package, 
            alpha_packages=alpha_packages,
            repo=repo,
            tag=tag
        ))
