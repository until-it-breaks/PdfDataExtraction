import json
import bisect
import sys
import time

from pathlib import Path

# Script used to fill a skeleton index with data from json files containing extracted data.
# Uses bisection to efficiently insert entries, therefore it's assumed that chapters in the skeleton are sorted.

def insert_page(items: dict, chapters: list, chapter_page_numbers: list, page_number: int):
    # skipping empty jsons "{}"
    if not items:
        print("INFO: {}.json is empty, skipping it".format(page_number))
        return

    index = find_page_chapter(chapters, chapter_page_numbers, page_number)

    if index is not None:
        chapter = chapters[index]
        if "data" not in chapter:
            chapter["data"] = {}

        for key, value in items.items():
            chapter["data"].update({key : value})
        print("INFO: {}.json has been inserted.".format(page_number))

def find_page_chapter(chapters: list, chapter_page_numbers: list, page_number: int):
    index = bisect.bisect(chapter_page_numbers, page_number)
    if (index < len(chapters) and chapters[index].get("pagina") == page_number):
        return index
    else:
        if (index > 0):
            return index - 1
        else:
            return None

start_time = time.time()

if len(sys.argv) < 4:
    print("USAGE: python fill_index.py <target_json> <pages_folder> <output_name>")
    sys.exit(1)

target_json = Path(sys.argv[1])
pages_folder = Path(sys.argv[2])
output_name = Path(sys.argv[3])

output = {}
chapters = []

with open(target_json, "r", encoding="utf-8") as f:
    output = json.load(f)

chapters = output.get("capitoli")
chapter_page_numbers = [chapter.get("pagina") for chapter in chapters]

pages = [f for f in pages_folder.iterdir() if f.is_file() and f.suffix == ".json"]

for page in pages:
    with open(page, "r", encoding="utf-8") as f:
        item = json.load(f)
        insert_page(item, chapters, chapter_page_numbers, int(page.stem))

with open(output_name, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii= False)
    print("INFO: Job done in {:.3f}s. Output at {}".format(time.time() - start_time, output_name.absolute()))