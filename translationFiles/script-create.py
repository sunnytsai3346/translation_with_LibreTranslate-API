
import os
from fnmatch import fnmatch
import xml.etree.cElementTree as ET
# creates new file and root for all language files
def createRoot(lang, fileName):
    tsfile = open(fileName,'x')
    root = ET.Element("TS",language=lang,sourcelanguage="en",version="2.1")
    tsfile = ET.ElementTree(root)
    tsfile.write(fileName, xml_declaration=True, encoding='utf-8')
    print("created "+ fileName)

createRoot('fo','FO.ts')
createRoot('en_US','EN.ts')
createRoot('de','DE.ts')
createRoot('es','ES.ts')
createRoot('fr','FR.ts')
createRoot('IT','IT.ts')
createRoot('JA','JA.ts')
createRoot('KO','KO.ts')
createRoot('PL','PL.ts')
createRoot('TS','PT.ts')
createRoot('RU','RU.ts')
createRoot('ZH','ZH.ts')
