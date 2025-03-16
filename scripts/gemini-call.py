from google import genai
import sys
import PIL.Image
import json
import re

def extract_json_content(text):
    match = re.search(r"```json\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return None

if (len(sys.argv) != 3):
    print("Make sure to add the image path and your Gemini API key")
    sys.exit()

image = PIL.Image.open(sys.argv[1])

key = sys.argv[2]
client = genai.Client(api_key=key)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["Analizza l'immagine. Estrai dati da tabelle, grafici o infografiche, se presenti, in formato JSON valido senza usare markdown. Se necessario, usa chiavi nella lingua nativa, inoltre cerca di essere sintetico con esse. Se non trovi dati rilevanti, ma solo intestazioni immagini o testo non strutturato, restituisci un JSON vuoto.", image],
)

extracted_json = extract_json_content(response.text)

try:
    data = json.loads(extracted_json)
    with open("output.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
except json.JSONDecodeError:
    print("Invalid JSON\n: {}".format(response.text))
