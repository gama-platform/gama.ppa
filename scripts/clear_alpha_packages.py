import os 
import apt_pkg

# This script is called to purge the alpha packages from: 
# 1. The Packages file
# 2. The repository


apt_pkg.init()

packagefile_old_content = []
packagefile_new_content = []

with open('Packages', 'r') as f:
    packages = apt_pkg.TagFile(f)
    for pkg in packages:
        packagefile_old_content.append(pkg)
        if pkg['Package'].endswith('alpha'):
            os.remove(pkg['Filename']) # 2
            pass
        else:
            packagefile_new_content.append(pkg)

with open('Packages', 'w') as fw:
    for pkg in packagefile_new_content:
        fw.write(str(pkg))