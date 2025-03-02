from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

images = convert_from_path("BS2024.pdf", thread_count=20)
for i in range(len(images)):
    images[i].save("page" + str(i) + ".jpg", "JPEG")