import json
import sys
import time

from pathlib import Path

# Script used to generate a review file out of a folder of files.

start_time = time.time()

if (len(sys.argv) < 2):
    print("USAGE: python create_review_file.py <folder-path>")
    sys.exit(1)

target = Path(sys.argv[1])

reviews = {}

for f in [f for f in target.iterdir() if f.is_file()]:
    reviews.update({"{}".format(f.name) : ""})

output_path = target.parent / (target.name + "-review.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(reviews, f, indent=4)

print("INFO: Job done in {:.3f}s. Output at {}".format(time.time() - start_time, output_path.resolve()))