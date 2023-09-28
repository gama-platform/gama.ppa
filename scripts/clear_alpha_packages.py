import os 

packages = open("Packages").read().split("\n\n")
if not packages[-1].strip():
    packages.pop()

packages_file_to_write = ""

for package in packages:
    
    package_lines = package.split("\n")

    print(package_lines)

    package_info = { p.split(": ")[0]: p.split(": ")[1] for p in package_lines}

    if package_info['Package'].endswith("alpha"):
        os.remove(package_info["Filename"])
    else:
        packages_file_to_write += package + "\n\n"

open("Packages", "w").write(packages_file_to_write)