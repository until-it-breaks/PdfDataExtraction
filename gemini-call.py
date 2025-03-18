import sys
import json
import re

from pathlib import Path
from PIL import Image
from google import genai

OUTPUT_FOLDER_NAME = "output"
PROMPT = (
    "Analizza l'immagine. Estrai dati da tabelle, grafici o infografiche, se presenti, in formato JSON valido. "
    "Se necessario, usa chiavi nella lingua nativa, inoltre cerca di essere sintetico con esse. "
    "Se non trovi dati rilevanti, ma solo intestazioni, immagini o testo non strutturato, restituisci un JSON vuoto."
)
MODEL = "gemini-2.0-flash"

def extract_json_content(text):
    """Extracts JSON content enclosed in triple backticks from text."""
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    return match.group(1).strip() if match else None

def main():

    if (len(sys.argv) != 3):
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