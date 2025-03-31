import base64
import sys
import os
import time

from ollama import chat
from ollama import ChatResponse
from pathlib import Path

PROMPT = (
    """
    Analizza l'immagine fornita, che fa parte di un bilancio di sostenibilità. Il tuo obiettivo è estrarre dati strutturati rilevanti per la valutazione delle performance di sostenibilità dell'azienda.
    Criteri di rilevanza:
    - Concentrati su tabelle, grafici e infografiche che presentano dati numerici (percentuali, valori monetari, indicatori di performance).
    - Escludi slide che contengono esclusivamente, indici o sommari, informazioni di contatto , introduzioni generiche, immagini senza dati numerici , solo titoli o intestazioni, crediti o ringraziamenti
    Output:
    - Estrai i dati in JSON valido e ben strutturato.
    - Usa le chiavi in snake_case, senza spazi o accenti, in lingua italiana. Per i valori non numerici mantieni il formato originale.
    - Struttura i dati in modo gerarchico, usando array e oggetti quando necessario.
    - Usa interi o float a seconda dei valori numerici che trovi.
    - Mantieni le percentuali come stringhe.
    - Per le posizioni cardinali usa solo interi.
    - Separa le unità di misura dai valori numerici, salvandoli a parte se presenti (`322.561.252,71 euro` → `322561252.71`).
    - Assegna titoli significativi ai dati estratti, evitando prefissi come `"figura"`, `"tabella"`, etc.
    - Se l'immagine non soddisfa i criteri di rilevanza, restituisci un JSON vuoto: `{}`.
    """
)

if (len(sys.argv) < 4):
	print("Usage: python script_name image_folder start_index model")
	sys.exit(1)

TARGET_FOLDER = sys.argv[1]
START_INDEX = sys.argv[2]
MODEL = sys.argv[3]

main_dir = Path(__file__).parent.resolve()
output_dir = main_dir / (Path(TARGET_FOLDER).stem + "-" + MODEL)
output_dir.mkdir(parents=True, exist_ok=True)

image_paths = [os.path.abspath(os.path.join(TARGET_FOLDER, f)) for f in os.listdir(TARGET_FOLDER)]
length = len(image_paths)

start_time = time.time()

for i in range(int(START_INDEX), length):
	with open(image_paths[i], "rb") as image_file:
		base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
		response: ChatResponse = chat(model=MODEL, messages=[
			{
				"role": "user",
				"content": PROMPT,
				"images": [str(base64_encoded)]
			},
		])

		output_path = output_dir / (Path(image_paths[i]).stem + ".txt")
		with open(output_path, "w", encoding="utf-8") as f:
			f.write(response.message.content)
			print("Output saved at {}".format(output_path))
			end_time = time.time()
			print("Time taken {:.3f}s".format(end_time - start_time))
		
		start_time = time.time()
