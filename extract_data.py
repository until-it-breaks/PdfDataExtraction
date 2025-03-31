import os
import subprocess
import sys
import time

# Script used to send API requests to Gemini 2 in bulk.

# Gemini 2 Flash daily limits
RPM = 15
RPD = 1500

MINUTE = 60
EXTRA_TIME = 10

def cls():
    os.system("cls" if os.name == "nt" else "clear")

api_key = sys.argv[1]

images = [os.path.abspath(os.path.join("images", f)) for f in os.listdir("images")]
length = len(images)

start_time = time.time()
count = 0
processes = []

for i in range(length):
    if (count == RPM):
        print("Waiting {}s before next batch".format(MINUTE + EXTRA_TIME))
        time.sleep(MINUTE + EXTRA_TIME)
        count = 0

    process = subprocess.Popen(["python", "gemini_call.py", images[i], api_key])
    processes.append(process)
    count += 1

for process in processes:
    process.wait()

print("Job Done")