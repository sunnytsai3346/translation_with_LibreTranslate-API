import xml.etree.ElementTree as ET
import requests

# Load and parse the XML file
xml_file = ".\\xml\\de.xml"
tree = ET.parse(xml_file)
root = tree.getroot()

# LibreTranslate API endpoint (replace with your URL if different)
api_url = "http://localhost:5000/translate"

# Translation settings
source_lang = "en"  # Source language (e.g., English)
target_lang = "de"  # Target language (e.g., Spanish)

# Loop through each entry in the XML
for entry in root.findall("entry"):
    source_text = entry.find("source").text  # Get text to translate
    
    # Prepare the API request payload
    payload = {
        "q": source_text,
        "source": source_lang,
        "target": target_lang,
        "format": "text"
    }
    
    # Send request to LibreTranslate
    response = requests.post(api_url, data=payload)
    
    if response.status_code == 200:
        translated_text = response.json()["translatedText"]
        # Update the <target> tag with the translated text
        entry.find("target").text = translated_text
    else:
        print(f"Failed to translate '{source_text}': {response.status_code}")

# Save the updated XML to a new file
tree.write("translated_output.xml", encoding="utf-8", xml_declaration=True)

print("Translation complete! Check 'translated_output.xml'.")