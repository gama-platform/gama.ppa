import glob
import sys
import os

import apt_pkg

from jinja2 import Template 

apt_pkg.init()

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
tag = args[1] # for the stable version
alpha_tag = None 

if pre_release: # if this is a pre-release, then give tag the value of the current stable version
    alpha_tag = tag
    with open("Packages", "r") as fp:
        for p in apt_pkg.TagFile(fp):
            if not p["Package"].endswith("alpha"): # get the latest stable version
                tag = p["Version"]
                break


with open("templates/_headers_template", "r") as f:
    template_header = Template(f.read())

    alpha_packages = []
    latest_packages = []

    if pre_release:
        latest_packages = [ d[:-5] for d in glob.glob("*.deb.html") ]
        alpha_packages = glob.glob("*.deb")
    else:
        latest_packages = glob.glob("*.deb")
    

    with open("__site/_headers", "w") as fw:
        fw.write(template_header.render(
            latest_packages=latest_packages, 
            alpha_packages=alpha_packages,
            repo=repo,
            tag=tag,
            alpha_tag=alpha_tag
        ))

for deb in files:
    with open("templates/package_template", "r") as f:
        template_deb_file = Template(f.read())
        with open(f"{deb}.html", "w") as fw:
            fw.write(template_deb_file.render(repo=repo, tag=tag, file=deb))
