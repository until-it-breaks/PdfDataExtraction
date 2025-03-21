import sys
import json
import re

from pathlib import Path
from PIL import Image
from google import genai

OUTPUT_FOLDER_NAME = "gemini-output-raw"
PROMPT = (
    """
    Analizza l'immagine fornita, che fa parte di un bilancio di sostenibilità. Il tuo obiettivo è estrarre dati strutturati rilevanti per la valutazione delle performance di sostenibilità dell'azienda.

    Criteri di Rilevanza:

    * Concentrati su tabelle, grafici e infografiche che presentano dati numerici (ad esempio, percentuali, valori monetari, indicatori di performance).
    * Escludi slide che contengono esclusivamente:
        * Indici o sommari
        * Informazioni di contatto
        * Introduzioni generiche
        * Immagini senza dati di supporto
        * Solo titoli o intestazioni
        * Crediti o ringraziamenti

    Formato di Output:

    * Estrai i dati strutturati in formato JSON valido.
    * Utilizza le chiavi nella lingua originale dell'immagine.
    * Annida le chiavi se necessario per rappresentare la struttura dei dati.
    * Assegna titoli significativi ai dati estratti, evitando prefissi come "figura" o "tabella".
    * Se l'immagine non soddisfa i criteri di rilevanza sopra indicati, restituisci un JSON vuoto: `{}`.
    """
)
MODEL = "gemini-2.0-flash"

def extract_json_content(text):
    """Extracts JSON content enclosed in triple backticks from text."""
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

    if extracted_json is None:
        print("No JSON content extracted.")
        sys.exit(1)

    try:
        data = json.loads(extracted_json)
        main_dir = Path(__file__).parent.resolve()
        output_dir = main_dir / OUTPUT_FOLDER_NAME
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"{image_name}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"JSON successfully saved to: {output_path}")
    except json.JSONDecodeError:
        print(f"Invalid JSON:\n{response.text}")
        sys.exit(1)

if __name__ == "__main__":
    main()