from string import Template
import sys

args = sys.argv[1:]

if (len(args) < 3):
    print(f"usage: python {sys.argv[0]} <repository> <tag> <files_expresed_as_a_json_array_of_str>")
    exit(1)

files = args[-1]
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

    headers_rules += f"/{m['file']}.html\n\tContent-Disposition: attachment; filename=\"{filename}.deb\"\n\tLocation: https://github.com/${{ env.REPOSITORY }}/releases/download/${{ inputs.tag }}/{filename}\n\n"

headers = template_headers.substitute(headers_rules=headers_rules)
f = open("__site/_headers", "w")
f.write(headers)