import sys
import time
import threading

from pathlib import Path

import gemini_call

# Script used to send API requests to Gemini 2 in bulk.

RPM = 15 # Gemini 2 free tier allows 15 api calls per minute.
DELAY = 64 # Amount of seconds to wait before next batch.

start_time = time.time()

if (len(sys.argv) < 4):
    print("USAGE: python extract_data.py <image_folder_path> <output_folder_name> <Gemini_API_key>")
    sys.exit(1)

images_path = Path(sys.argv[1])
output_folder_name = sys.argv[2]
api_key = sys.argv[3]

images = [f for f in images_path.iterdir() if f.is_file()]
length = len(images)

call_count = 0
threads = []

for i, image_path in enumerate(images):
    print("INFO: Currently at {}/{} image(s). Processing {}.".format(i + 1, length, image_path))
    thread = threading.Thread(target=gemini_call.process_image, args=(image_path, output_folder_name, api_key))
    threads.append(thread)
    thread.start()
    call_count += 1

    if (call_count == RPM):
        print("INFO: Waiting {}s before next batch.".format(DELAY))
        time.sleep(DELAY)
        call_count = 0

for thread in threads:
    thread.join()

print("INFO: Job done in {:.3f}s.".format(time.time() - start_time))