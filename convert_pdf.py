import multiprocessing
import sys
import time

from tempfile import TemporaryDirectory
from pathlib import Path
from pdf2image import pdfinfo_from_path, convert_from_path

# A simple script that turns pdf pages into images.

OUTPUT_FOLDER_NAME = "images"
PAGE_COUNT_KEY = "Pages"

start_time = time.time()

if (len(sys.argv) < 2):
    print("USAGE: python convert_pdf.py <pdf_path>")
    sys.exit(1)

pdf_path = sys.argv[1]
pdf_info = pdfinfo_from_path(pdf_path=pdf_path)
pages_count = pdf_info[PAGE_COUNT_KEY]
threads = multiprocessing.cpu_count()

output_dir = (Path(__file__).parent / OUTPUT_FOLDER_NAME / Path(pdf_path).stem).resolve()
output_dir.mkdir(parents=True, exist_ok=True)

print("INFO: Converting {} pages from {} with {} threads.".format(pages_count, pdf_path, threads))

# Using a temporary directory yields better performance when using multiple threads
with TemporaryDirectory() as temp_folder:
    images = convert_from_path(pdf_path, thread_count=threads, output_folder=temp_folder)
    for i, image in enumerate(images, start=1):
        image.save(output_dir / "{}.jpeg".format(str(i).zfill(3)), "JPEG")

end_time = time.time()

print("INFO: Job done in {:.3f}s. Output at {}".format(end_time - start_time, output_dir))
