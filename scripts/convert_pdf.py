import multiprocessing, sys, os, time, tempfile, shutil
from pdf2image import pdfinfo_from_path, convert_from_path

if (len(sys.argv) == 1):
    print("Missing target PDF path")
    sys.exit()

pdf_path = sys.argv[1]
pdf_info = pdfinfo_from_path(sys.argv[1])
pages_count = pdf_info["Pages"]
threads = multiprocessing.cpu_count()

temp_folder = tempfile.mkdtemp() # Using a temporary directory yields better performance when using multiple threads
output_folder = "pages"

print("Beginning conversion of {pages} pages from {path} with {count} threads".format(pages=pages_count, path=pdf_path, count=threads))

start_time = time.time()

os.makedirs(output_folder, exist_ok=True)

images = convert_from_path(pdf_path, thread_count=threads, output_folder=temp_folder)

for i, image in enumerate(images, start=1):
    image_path = os.path.join(output_folder, "{}.jpeg".format(i))
    image.save(image_path, "JPEG")

end_time = time.time()

shutil.rmtree(temp_folder)

print("Job done in {:.3f}s".format(end_time - start_time))
print("You can find the output at {}".format(os.path.abspath(output_folder)))
