import subprocess
import os
import re


def build_list_of_files():
    stylus_files = []
    coffee_files = []
    for root, dirs, files in os.walk("."):
        for f in files:
            filepath = root + "/" + f
            if (re.match(r"^.*\.styl$", filepath)):
                stylus_files.append(filepath)
            elif (re.match(r"^.*\.coffee$", filepath)):
                coffee_files.append(filepath)
    return stylus_files, coffee_files


def run_compilers(stylus_files, coffee_files):
    for f in stylus_files:
        subprocess.Popen("stylus -w %s" % (f), shell=True)
    for f in coffee_files:
        subprocess.Popen("coffee -wc %s" % (f), shell=True)


if __name__ == "__main__":
    stylus_files, coffee_files = build_list_of_files()
    run_compilers(stylus_files, coffee_files)
