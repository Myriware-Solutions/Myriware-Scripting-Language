# import libraries
print("Importing Setup Python Libraries...")
import os
import shutil
import sys
import urllib.request
print("Done")
# remove all the old stuff
print("Removing old instances...")
try:
    shutil.rmtree("./msl/", ignore_errors=False, onerror=None)
except:
    print("Nothing to remove")
# create all the needed folders
print("Creating MSL Dirrectory...")
os.mkdir("msl/")
os.mkdir("msl/gen/")
os.mkdir("msl/imports/")
os.mkdir("msl/lang/")
print("Done")
# create classses file
print("Settingup Classes File (classes.json)")
classes_file = open('msl/classes.json', 'w')
classes_file.write("{ }")
classes_file.close()
# create config file
print("Settingup Configuration File (config.toml)")
config_file = open("msl/config.toml", 'w')
try:
    if sys.argv[1] != None:
        lang = sys.argv[1]
        print("Setting Lang to " + lang)
    else:
        lang = "en"
        print("Setting to English (no lang was found)")
except:
    lang = "en"
config = f"""pri = true
sec = false
err = true
net = true
lang = "{lang}"
tips = true
"""
print("Writting...")
config_file.write(config)
print("Done")
# import github materials for lang
print("Importing lang files...")
github_url = "https://raw.githubusercontent.com/Myriware-Solutions/mslimports/main/lang/"

urllib.request.urlretrieve(github_url + "_msl.sch", "msl/lang/_msl.sch")

print("imported schema")

urllib.request.urlretrieve(github_url + lang + '.lang', "msl/lang/" + lang + ".lang")

print("imported " + lang + " lang file")
print("Done")

print("Done with setup. Try running a .msl file with 'python msl.zip file <path>' or the live console 'python msl.zip console'")