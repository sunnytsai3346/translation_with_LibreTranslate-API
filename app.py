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
        # Extract target language from filename (e.g., "de" from "de.xml")
        target_lang = filename.split(".")[0].lower()  # Assumes format like "de.xml"
        
        # Full paths for input and output files
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        
        # Parse the XML file
        tree = ET.parse(input_path)
        root = tree.getroot()        
        # Translate each <source> tag and update <target>
        for context in root.findall("context"):            
            for message_entry in context.findall("message"):
                source_text = message_entry.find("source").text
                translation_tag = message_entry.find("translation").text
                # Check if the object has the attribute "type"
                if hasattr(message_entry, "type"):
                    unfinished = message_entry.attrib['type']
                    print(f"type:{unfinished}")
                else:
                    unfinished = ''
                
                if source_text:  # Ensure there’s text to translate
                    translated_text = translate_text(source_text, target_lang)
                    
                    if translated_text and unfinished == 'unfinished': 
                        print (f"{source_text}, {translate_text}")
                        message_entry.find("translation").text = translated_text
        
        # Save the updated XML to the target folder
        tree.write(output_path, encoding="utf-8", xml_declaration=True)
        print(f"Processed {filename} -> {output_path}")

print("All translations complete!")