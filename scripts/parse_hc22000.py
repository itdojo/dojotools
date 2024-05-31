#!/usr/bin/env python3

import glob
import os
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <folder_name>")
    sys.exit(1)
else:
    folder_name = sys.argv[1]

file_ext = "hc22000"


file_list = glob.glob(os.path.join(os.getcwd(), folder_name, f"*.{file_ext}"))

corpus = []

for file_path in file_list:
    with open(file_path) as f_input:
        corpus.append(f_input.read())

print(file_list)
