import os
import shutil

print("Removing old instance...")
try:
    os.remove("msl.zip")
except:
    print("Nothing to remove")
print("Zipping work...")
shutil.make_archive("msl", 'zip', "py")

def set():
    print("Done. Running Setup...")
    os.system("python setup.py")

#set()
os.system("python msl.zip console")

