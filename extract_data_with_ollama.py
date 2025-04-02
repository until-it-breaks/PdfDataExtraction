import base64
import sys
import time

from ollama import chat
from ollama import ChatResponse
from pathlib import Path

PROMPT = """
    Analizza l'immagine fornita, che fa parte di un bilancio di sostenibilità. Il tuo obiettivo è estrarre dati strutturati rilevanti per la valutazione delle performance di sostenibilità dell'azienda.
    Criteri di rilevanza:
    - Concentrati su tabelle, grafici e infografiche che presentano dati numerici (percentuali, valori monetari, indicatori di performance).
    - Escludi slide che contengono esclusivamente indici o sommari, informazioni di contatto, introduzioni generiche, immagini senza dati numerici, solo titoli o intestazioni, crediti o ringraziamenti.
    Per quanto riguarda l'output:
    - Estrai i dati in JSON valido e ben strutturato.
    - Usa le chiavi in snake case, senza spazi o accenti, in lingua italiana. Per i valori non numerici mantieni il formato originale.
    - Struttura i dati in modo gerarchico, usando array e oggetti quando necessario.
    - Usa interi o float a seconda dei valori numerici che trovi.
    - Mantieni le percentuali come stringhe.
    - Per le posizioni cardinali usa solo interi.
    - Separa le unità di misura dai valori numerici, salvandoli a parte se presenti (`322.561.252,71 euro` -> `322561252.71`).
    - Assegna titoli significativi ai dati estratti, evitando prefissi come `"figura"`, `"tabella"`, etc.
    - Se l'immagine non soddisfa i criteri di rilevanza, restituisci un JSON vuoto: `{}`.
    """

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
	with open(images[i], "rb") as image_file:
		base64_image = base64.b64encode(image_file.read()).decode("utf-8")
		response: ChatResponse = chat(model=model, messages=[
			{
				"role": "user",
				"content": PROMPT,
				"images": [base64_image]
			},
		])

		output_path = output_dir / (images[i].stem + ".txt")
		with open(output_path, "w", encoding="utf-8") as f:
			time_taken = time.time() - start_time
			f.write("INFO: Job done in {:.3f}s.\n".format(time_taken))
			f.write(response.message.content)
			print("INFO: Job done in {:.3f}s. Output at {}".format(time_taken, output_path.resolve()))