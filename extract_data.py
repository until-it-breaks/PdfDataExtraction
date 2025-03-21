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

api_key = sys.argv[1]

images = [os.path.abspath(os.path.join("images", f)) for f in os.listdir("images")]
length = len(images)

start_time = time.time()
count = 0
processes = []

for i in range(length):
    if (count == RPM):
        print("Waiting a {}s before next batch".format(MINUTE + EXTRA_TIME))
        time.sleep(MINUTE + EXTRA_TIME)
        count = 0

    process = subprocess.Popen(["python", "gemini-call.py", images[i], api_key])
    processes.append(process)
    # print("Progress: {:.1f}%".format((i+1) / length * 100))
    count += 1

for process in processes:
    process.wait()

print("Job Done")