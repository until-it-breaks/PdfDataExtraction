from PyPDF2 import PdfReader

reader = PdfReader("../BS2024.pdf")
with open("pypdf_output.txt", "a", encoding="utf-8") as f:
    for page in reader.pages:
        f.write("###########Page %s###########\n" % reader.get_page_number(page))
        print("Extracting page %s" % reader.get_page_number(page))
        f.write(page.extract_text())
        f.write("\n")