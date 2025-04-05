# PdfDataExtraction

First of a bit of a backstory, I was assigned the task to extract data from a Sustainability Report without any source whatsoever. Such file contains a huge amount of graphs, table, charts and infographics which of course hold the most interesting pieces of data.
Some examples:
<img src="./images/BS2024/011.jpeg" alt="Image containing infographics" width="300" height="200">
<img src="./images/BS2024/080.jpeg" alt="Image containing a bar chart" width="300" height="200">

The PDF in question contains about 228 pages so extracting data manually was not an option.
Traditional OCR methods required to much in-depth knowledge which I lacked and I would have liked to automatize such task as much as possible.
I even scoured to no avail cloud suites such as Azure but nothing seemed to be good enough or tailored for such task.
The solution seemed to be LLM and ChatGPT seemed a good candidate, specifically GPT4-o.
The model itself did yield good results with some flaws though. First of all it was clear that LLMs are still not good enough at correcly assigning trivial labels to data extracted from an images, often time swapping among two. Other times it would mislabel by just one step due to outliers in the infographics format.
That was good enough for me and I immediately thought about using the API to process the images in bulk but sadly such service follows a pay-as-you-go price model.

It was then that I found about Gemini 2 Flash from Google which offers an LLM that is just as good with API support too. Such API has a free tier that allows up to 15 calls per minute and 1500 calls per day which are plenty enough for my purpose.

From there I started creating some scripts to use the API.

However, the free tier of Gemini 2 states that the data from the interactions is used to further train their models. One could argue that for the sake of privacy they'd like to avoid such option, especially with a big corporation such as Google.

It's for this reason that I also discovered about the possibility to host LLM locally via a user friendly program called Ollama. Such project is open-source and allows the download of various models to use locally on your own pc without any internet connection.
The models come with many versions, some are bigger in terms of parameter count (b) and require more memory.
Generally speaking, the best scenario is that the host pc is equipped with a strong GPU with lots of VRAM (more than 8GB) but the model itself can be either fully or partially offloaded to the CPU which can greatly slow down the speed of inference.
Although not getting results as good as the ones I got from commercial LLM like Gemini and GPT4-o I still wrote a script to process images with the Ollama API. My machine is not up to the task since it has just 16GB of RAM and 8GB of VRAM and the lighter models tend to not perform well with complex prompt. One could definitely get better results with bigger models such as Gemma 3 in its better variants.

The purpose of this repository is to host scripts used to extract data from PDFs using LLM solutions.

First of all you have to split the PDF's pages into images.
Each image will then be fed with a prompt to either Gemini 2 or a vision capable LLM hosted locally with ollama.
The former solution is fast, and requires an API key which you can get for free. The latter requires good hardware, preferrably a GPU with more than 8GB of VRAM.

The process is simple. The first step is turning the PDF file into images, JPEG is preferrable since they require less space.
Then it's required to create a structured index file with each chapter and their corresponding page number.
The images will be then fed to a LLM with a prompt one by one, asking in return a json file containing the extracted data.
Once that's done each individual json will be merged into the index one by matching the page number.

The basic workflow is to convert the pdf pages into images, call Gemini 2 to extract data from each of those images, ready up an index file with chapters and their corresponding page numbers and then fill such file with the output files from Gemini 2.

## Convert a PDF to images
Run `python convert_pdf.py <pdf_path>` where `<pdf_path>` is the path of the target PDF.

Requires `pdf2image` library which you can install with `pip install pdf2image`. `poppler` is also required, the details about its installation can be found at https://pypi.org/project/pdf2image

## Extracting data from a single image with Gemini 2
Run `python gemini_call.py <image_path> <output_folder_name> <Gemini_API_key>` where `<image_path>` is the path of the target image, `output_folder_name` is the name of the folder from the current working directory and `<Gemini_API_key>` is your personal Gemini 2 API key.

Requires `google-genai` library which you can install with `pip install google-genai` as well as `pillow` which should come with `poppler` but can be installed with `pip install pillow`.

Note: The prompt can be changed by editing the `PROMPT` variable in the script.

## Extract data from images in bulk
Run `python extract_data.py <image_folder_path> <output_folder_name> <Gemini_API_key>` where `<image_path>` is the path of the target image, `output_folder_name` is the name of the folder from the current working directory and `<Gemini_API_key>` is your personal Gemini 2 API key.

Requires `google-genai` library which you can install with `pip install google-genai` as well as `pillow` which should come with `poppler` but can be installed with `pip install pillow`.

Note: As of April 2025, Gemini 2 free tier allows up to 15 request per minute and 1500 requests per day. That may change in the future and you can easily tweak those values in the script.

## Complete an index file
Run `python fill_index.py <target_json> <pages_folder> <output_name>` where `<target_json>` is the path to the index file that needs to be filled, `<pages_folder>` is the folder containing the json files containing extracted data from a specific page and `<output_name>` is the name of the final output file in json format.

## Extract data from images with Ollama API
Run `python extract_data_with_ollama.py <images_folder> <start_index> <model>` where `<images_folder>` is the path of the folder containing the images from which to extract data, `<start_index>` is the index of the image from which to start (`0` means start from the first), assuming that the images are sorted numerically and `<model>` is the name of the model you pulled with Ollama.

Requires `ollama` library which you can install with `pip install ollama`

Note: The prompt can be changed by editing the `PROMPT` variable in the script. In order for the script to work you need to have Ollama serving and have the models available. Results may vary depending on the models choosen and their parameter and context length configuration. Bigger models require a lot of memory, if the GPU(s) is not powerful enough or does not have enough of VRAM, part of the workload is offloaded onto CPU and RAM, whcih greatly slows down the process.