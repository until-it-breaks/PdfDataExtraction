# PdfDataExtraction

The purpose of this repository is to host scripts used to extract data from PDFs using LLM solutions.

First of all you have to split the PDF's pages into images.
Each image will then be fed with a prompt to either Gemini 2 or a vision capable LLM hosted locally with ollama.
The former solution is fast, and requires an API key which you can get for free. The latter requires good hardware, preferrably a GPU with more than 8GB of VRAM.