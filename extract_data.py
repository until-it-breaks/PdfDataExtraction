import os
import subprocess
import sys
import time

# Gemini 2 Flash daily limits
RPM = 15
RPD = 1500

MINUTE = 60
EXTRA_TIME = 10

def cls():
    os.system("cls" if os.name == "nt" else "clear")

API_KEY = sys.argv[1]

pages = [os.path.abspath(os.path.join("images", f)) for f in os.listdir("images")]
length = len(pages)

count = 0
start_time = time.time()

for i in range(length):
    if (count == RPM):
        elapsed = time.time() - start_time
        if (elapsed < MINUTE):
            time.sleep(MINUTE + EXTRA_TIME - elapsed)
        count = 0
        start_time = time.time()

    subprocess.run(["python.exe", "scripts/gemini-call.py", pages[i], API_KEY])
    print("Progress: {:.1f}%".format((i+1) / length * 100))
    count += 1

print("Job Done")