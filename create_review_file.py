import json
import os
import sys
import time

# Script used to generate a review file out of a folder of jsons.

if (len(sys.argv) < 2):
    print("USAGE: python create-review-file.py <folder-path>")
    sys.exit(1)

target = sys.argv[1]

start_time = time.time()

reviews = {}
for f in [f for f in os.listdir(target) if f.endswith(".json")]:
    reviews.update({"{}".format(f) : ""})

with open("{}-review.json".format(target), "w", encoding="utf-8") as f:
    json.dump(reviews, f, indent=4)

print("INFO: Job done in {:.3f}s.".format(time.time() - start_time))