import os
import time
import subprocess
import sys

# Gemini 2 Flash daily limits
RPM = 15
RPD = 1500

def cls():
    os.system("cls" if os.name == "nt" else "clear")


API_KEY = sys.argv[1]

pages = os.listdir("pages")
length = len(pages)

# Slow down the script

for i in range(length):
    subprocess.run(["python.exe", "scripts/gemini-call.py", pages[i], API_KEY])
    cls()
    print("Progress: {:.1f}%".format(i / length * 100))

cls()
print("Job Done")