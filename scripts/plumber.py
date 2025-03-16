import pdfplumber

with pdfplumber.open("BS2024.pdf") as pdf:
    with open("output_plumber.txt", "a", encoding="utf-8") as f:
        for page in pdf.pages:
            f.write("###########Page %s###########\n" % page.page_number)
            print("Extracting page %s" % page.page_number)
            f.write(page.extract_text())
            f.write("\n")