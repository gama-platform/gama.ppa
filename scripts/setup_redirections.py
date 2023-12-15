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
