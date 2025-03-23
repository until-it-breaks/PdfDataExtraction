import sys
import json
import re

from pathlib import Path
from types import NoneType
from PIL import Image
from google import genai

# Script used to make a single API call to Gemini 2.

OUTPUT_FOLDER_NAME = "gemini-output-raw"
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
MODEL = "gemini-2.0-flash"

def extract_json_content(text):
    # Extracts JSON content enclosed in triple backticks from text.
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    return match.group(1).strip() if match else None

def main():

    if (len(sys.argv) < 3):
        print("Usage: python gemini-call.py <image_path> <Gemini_API_key>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    api_key = sys.argv[2]

    if not image_path.exists():
        print(f"Error: The file '{image_path}' does not exist.")
        sys.exit(1)

    image_name = image_path.stem

    with Image.open(image_path) as image:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL,
            contents=[PROMPT, image],
        )

    extracted_json = extract_json_content(response.text)

    main_dir = Path(__file__).parent.resolve()
    output_dir = main_dir / OUTPUT_FOLDER_NAME
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{image_name}.json"

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            if extracted_json is None or extracted_json is NoneType:
                json.dump({}, f, indent=4, ensure_ascii=False)
                print("No JSON content extracted.")
            else:
                data = json.loads(extracted_json)
                json.dump(data, f, indent=4, ensure_ascii=False)
                print(f"JSON successfully saved to: {output_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON:\n{response.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()