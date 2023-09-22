import json
from string import Template
import sys
import os

args = sys.argv[1:]

pre_release = False
p_flag_index = -1

print(args)
for i, a in enumerate(args):
    if pre_release:
        pass
    if a == "-p" or a == "--pre-release":
        pre_release = True
        p_flag_index = i

if pre_release:
    args.pop(p_flag_index)


if (len(args) < 3):
    print(f"usage: python {sys.argv[0]} [-p|--pre-release] <repository> <tag> <files_expresed_as_a_json_array_of_str>")
    print( "    -p, --pre-release: use this flag to indicate that the tag is a pre-release, and that the following json array of strings is the related files")
    exit(1)

print(args[-1])

files = json.loads(args[-1])
mappings = []
headers_rules = ""

for file in files:
    redirect_target = file.split("/")[-1]

    print(redirect_target)

    mappings.append(
        { "repo": args[0], "tag": args[1], "file": redirect_target }
    )

template_deb_file = Template(open("templates/package_template").read())
template_headers  = Template(open("templates/_headers_template").read())

for m in mappings:
    content = template_deb_file.substitute(**m)
    f = open(f"{m['file']}.html", "w")
    f.write(content)
    filename = m["file"].split("/")[-1].split(".html")[0]

    headers_rules += f"/{m['file']}.html\n\tContent-Disposition: attachment; filename=\"{filename}.deb\"\n\tLocation: https://github.com/{ args[0] }/releases/download/{args[1]}/{filename}\n\n"


# if it is a prerelease we just append to an existing _headers file
if not pre_release or not os.path.isfile("__site/_headers"):
    headers = template_headers.substitute(headers_rules=headers_rules)
    f = open("__site/_headers", "w")
    f.write(headers)
else:
    f = open("__site/_headers", "a")
    f.write(headers_rules)
