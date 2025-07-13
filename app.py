import os
import xml.etree.ElementTree as ET
import requests

# Load and parse the XML file
input_folder = "xml"
output_folder = "target"
# LibreTranslate API endpoint 
api_url = "http://127.0.0.1:5000/translate"
source_lang = "en"  # Source language (e.g., English)

# Create output folder if it doesn’t exist
os.makedirs(output_folder, exist_ok=True)


# Function to translate text via LibreTranslate
def translate_text(text, target_lang):
    payload = {
        "q": text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    response = requests.post(api_url, data=payload)
    if response.status_code == 200:
        return response.json()["translatedText"]
    else:
        print(f"Failed to translate '{text}' to {target_lang}: {response.status_code}")
        return None

#Process each XML file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".ts"):
        translated_count = 0
        # Extract target language from filename (e.g., "de" from "de.xml")
        target_lang = filename.split(".")[0].lower()  # Assumes format like "de.xml"
        
        # Full paths for input and output files
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Parse the XML file
        tree = ET.parse(input_path)
        root = tree.getroot()        
        # Translate each <source> tag and update <target>
        for message in root.findall(".//message"):            
            source_elem = message.find("source")
            translation_elem = message.find("translation")

            if source_elem is not None and translation_elem is not None:
                source_text = source_elem.text.strip() if source_elem.text else ""
                translated_type = translation_elem.get("type")

                if translated_type =='unfinished' and source_text:
                    translated_text = translate_text(source_text, target_lang)
                    translation_elem.text = translated_text
                    del translation_elem.attrib['type']
                    translated_count +=1
                    print(f"Translated: '{source_text} -> {translated_text}")
                
                
    
        # Save the updated XML to the target folder
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"\nProcessed {translated_count} translations . {filename} -> {output_path}")

print("All translations complete!")