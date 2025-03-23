import json
import os
import bisect
import time

# Script used to fill an index skeleton with data from json files containing extracted data.
# Uses bisection to efficiently insert entries, therefore it's assumed that chapters in the skeleton are sorted.

INDEX_FILE = "index-skeleton.json"
OUTPUT_FILE = "index.json"
PAGES_FOLDER = "gemini-output-reviewed"

def insert_page(item: dict, page_number: int):
    # skipping empty jsons "{}"
    if not item:
        print("{}.json is empty, skipping it".format(page_number))
        return

    index = find_page_chapter(chapters, page_number)

    if index is not None:
        chapter = chapters[index]
        if "data" not in chapter:
            chapter["data"] = []

        for key, value in item.items():
            chapter["data"].append({
                "topic": key,
                "items": value
            })
        print("{}.json has been inserted".format(page_number))

def find_page_chapter(chapters, page_number: int):
    index = bisect.bisect(chapter_page_numbers, page_number)
    if (index < len(chapters) and chapters[index].get("pagina") == page_number):
        return index
    else:
        if (index > 0):
            return index - 1
        else:
            return None

start_time = time.time()

source = {}
chapters = []

with open(INDEX_FILE, "r", encoding="utf-8") as f:
    source = json.load(f)

chapters = source.get("capitoli")
chapter_page_numbers = [chapter.get("pagina") for chapter in chapters]

pages = [f for f in os.listdir(PAGES_FOLDER) if f.endswith(".json")]

for page in pages:
    with open(os.path.join(PAGES_FOLDER, page), "r", encoding="utf-8") as f:
        item = json.load(f)
        page_number = (int) (page.split(".")[0])
        insert_page(item, page_number)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(source, f, indent=4, ensure_ascii= False)
    end_time = time.time()
    print("Job done in {:.3f}s. Output at {}".format(end_time - start_time, os.path.join(os.getcwd(), OUTPUT_FILE)))