import os
from fnmatch import fnmatch
import xml.etree.cElementTree as ET
#root = ET.Element("TS",language="en_US",sourcelanguage="en",version="2.1")
#context = ET.SubElement(root, "context")
# ET.SubElement(doc, "field1", name="blah").text = "some value1"
# ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

# tree = ET.ElementTree(root)
# tree.write("script-data.ts")

global pageLink
global userLevel
global stringName
global stringComment
global newContext

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

def translateFiles(tsFileName, oldTsFileName):
    print ("Searching for strings in Fusion translation files for " + tsFileName + "...")
    scriptFile = ET.parse(tsFileName)
    scriptFileRoot = scriptFile.getroot()
    oldScriptFile = ET.parse(oldTsFileName)
    oldScriptFileRoot = oldScriptFile.getroot()

    # read all the directories and sub-directories from the specified folder
    messageAdded = False
        
    # file has exisiting context, checks for the same context name against file name
    for srcContext1 in scriptFileRoot.findall('context'):
        for srcContext in srcContext1.findall('message'):
            for oldSrcContext1 in oldScriptFileRoot.findall('context'):
                for oldSrcContext in oldSrcContext1.findall('message'):
                    if (srcContext.find('source').text == oldSrcContext.find('source').text):
                        oldSrcContextTranslation = oldSrcContext.find('translation');
                        if(oldSrcContext.find('translation').text):
                            if(oldSrcContextTranslation.find('numerusform') != None):
                                # print (oldSrcContextTranslation.find('numerusform'))                                
                                srcContext.find('translation').text = oldSrcContextTranslation.find('numerusform').text;
                                srcContext.find('translation').attrib.pop('type', None)
                            else:
                                srcContext.find('translation').text = oldSrcContext.find('translation').text;
                                srcContext.find('translation').attrib.pop('type', None)
                        else:
                            # print ("i am here")
                            srcContext.find('translation').text = ' ';
                            
    scriptFile = ET.ElementTree(indent(scriptFileRoot))
    scriptFile.write(tsFileName, xml_declaration=True, encoding='utf-8')                        



translateFiles('DE.ts', 'OldFusionFiles/fusionuiapp_de.ts')
translateFiles('ES.ts', 'OldFusionFiles/fusionuiapp_es.ts')
translateFiles('FR.ts', 'OldFusionFiles/fusionuiapp_fr.ts')
translateFiles('IT.ts', 'OldFusionFiles/fusionuiapp_it.ts')
translateFiles('JA.ts', 'OldFusionFiles/fusionuiapp_ja.ts')
translateFiles('KO.ts', 'OldFusionFiles/fusionuiapp_ko.ts')
translateFiles('PL.ts', 'OldFusionFiles/fusionuiapp_pl.ts')
translateFiles('PT.ts', 'OldFusionFiles/fusionuiapp_pt.ts')
translateFiles('RU.ts', 'OldFusionFiles/fusionuiapp_ru.ts')
translateFiles('ZH.ts', 'OldFusionFiles/fusionuiapp_zh.ts')