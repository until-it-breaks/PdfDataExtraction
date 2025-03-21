import json
import os
import sys

if (len(sys.argv) < 2):
    print("Usage: python create-review-file.py <folder-path>")
    exit(1)

FOLDER = sys.argv[1]

reviews = {}
for f in os.listdir(FOLDER):
    reviews.update({"{}".format(f) : ""})

with open("{}-review.json".format(FOLDER), "w", encoding="utf-8") as f:
    json.dump(reviews, f, indent=4)

print("Job done")