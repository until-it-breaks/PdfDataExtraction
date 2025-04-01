import sys
import json
import re
import time

from pathlib import Path
from PIL import Image
from google import genai

# Script used to make a single API call to Gemini 2.

DEBUG_FOLDER_NAME = "raw"
MODEL = "gemini-2.0-flash"
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

def extract_json(text):
    # Extracts JSON content enclosed in triple backticks from text.
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    return match.group(1).strip() if match else None

def process_image(image_path, output_folder_name, api_key):
    start_time = time.time()

    image_path = Path(image_path)

    if not image_path.exists():
        print("ERROR: The file {} does not exist".format(image_path))
        return

    with Image.open(image_path) as image:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL,
            contents=[PROMPT, image],
        )

        cwd = Path(__file__).parent
        output_dir = cwd / output_folder_name
        raw_dir = cwd / output_folder_name / DEBUG_FOLDER_NAME

        output_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / "{}.json".format(image_path.stem)
        raw_path = output_dir / DEBUG_FOLDER_NAME / "{}.txt".format(image_path.stem)

        with open(raw_path, "w", encoding="utf-8") as f:
            f.write("INFO: Job done in {:.3f}s.\n".format(time.time() - start_time))
            f.write("Raw response:\n{}".format(response))

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                data = json.loads(extract_json(response.text))
                json.dump(data, f, indent=4, ensure_ascii=False)
                print("INFO: JSON successfully saved at {}".format(output_path))
        except:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
                print("ERROR: No JSON content extracted from {}".format(image_path))

if __name__ == "__main__":
    if (len(sys.argv) < 4):
        print("USAGE: python gemini-call.py <image_path> <output_folder_name> <Gemini_API_key>")
    else:
        process_image(sys.argv[1], sys.argv[2], sys.argv[3])