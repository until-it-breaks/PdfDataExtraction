import sys
import time

from ollama import chat
from ollama import ChatResponse
from pathlib import Path

PROMPT = "Cosa c'è nell'immagine? Se ci sono dati numerici, ritornami un json strutturato. Altrimenti ritorna un json vuoto"

if (len(sys.argv) < 4):
	print("USAGE: python extract_data_with_ollama.py <images_folder> <start_index> <model>")
	sys.exit(1)

images_folder = Path(sys.argv[1])
start_index = int(sys.argv[2])
model = sys.argv[3]

cwd = Path(__file__).parent
output_dir = cwd / "results" / (images_folder.stem + "-" + model.replace(":", ""))
output_dir.mkdir(parents=True, exist_ok=True)

images = [f for f in images_folder.iterdir() if f.is_file()]

for i in range(start_index, len(images)):
	start_time = time.time()
	response: ChatResponse = chat(model=model, messages=[
		{
			"role": "user",
			"content": PROMPT,
			"images": [images[i].resolve()]
		},
	])

	output_path = output_dir / (images[i].stem + ".txt")
	with open(output_path, "w", encoding="utf-8") as f:
		time_taken = time.time() - start_time
		f.write("INFO: Job done in {:.3f}s.\n".format(time_taken))
		f.write(response.message.content)
		print("INFO: Job done in {:.3f}s. Output at {}".format(time_taken, output_path.resolve()))