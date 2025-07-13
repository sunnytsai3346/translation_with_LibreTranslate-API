# Extract all the strings from the specified translation 
# files (*.ts), converting it to the json format used by the WebUI and writing those
# files out to the jsonDir (aka *.ts to ../src/translations/*.json).
#
# Run this (Python 3) script by opening a command window in this directory 
# (<SHIFT>+<RIGHT CLICK> + Open command window here)
# At the prompt, type:
#   py ts2Json.py

import os, glob
from fnmatch import fnmatch
import xml.etree.cElementTree as ET
from operator import itemgetter

def writeJSONEntry(srcMessage, destFile, srcContextName, srcfileName):
    sourceTextString = srcMessage.find('source').text
    sourceTextKey = srcMessage.find('source').text.replace(' ', '').replace('\n', '').replace('"', '\\"')
    nameTextStatus = srcContextName.find('name').text
    statuslist = ['automation.component.ts',
    'contentValidation.component.ts','edr.component.ts',
    'fans.component.ts','lamp.component.ts',
    'laser.component.ts','network.component.ts',
    'photon.component.ts','playback.component.ts',
    'preferences.component.ts','scheduler.component.ts',
    'security.component.ts','system.component.ts',
    'temperature.component.ts','versions.component.ts',
    'video.component.ts','lens.component.ts',
    'values.component.ts','rental.component.ts', 'serial.component.ts'
    ]

    res = any(ele in nameTextStatus for ele in statuslist)
    nameText = srcContextName.find('name').text.replace(".ts", "")
    nameText = nameText.replace(".", "")
    nameText = nameText.replace("-", "")
    if(res):
        nameText = 'statusitemcomponent'
    translationText = srcMessage.find('translation').text.replace('\n', '\\n').replace('"', '\\"')
    if (srcfileName == "EN.ts"):
        destFile.write('\n    \"' + nameText + sourceTextKey + '": "' + sourceTextString.replace('\n', '\\n').replace('"', '\\"') + '"')
    elif (srcfileName == "FO.ts"):
        destFile.write('\n    \"' + nameText + sourceTextKey + '\": \"' + '*' + sourceTextString.replace('\n', '\\n').replace('"', '\\"') + '*' + '\"')
    else:
        if(translationText == ' '):
            destFile.write('\n    \"' + nameText + sourceTextKey + '\": \"' + '\"')
        else:
            destFile.write('\n    \"' + nameText + sourceTextKey + '\": \"' + translationText + '\"')

jsonDir = "JsonFiles" + os.sep

for srcFile in glob.glob( "*.ts" ):
    tsFile = ET.parse( srcFile )
    root = tsFile.getroot()

    # build up the destination file + path
    destFileName = jsonDir + srcFile.replace('.ts', '.json')
    print( "Converting from " + srcFile + " to " + destFileName )
    with open(destFileName, 'w', encoding="utf-8") as destFile:
        destFile.write("{") # open file with curly brace
        # add all the names of contexts to a list 
        list = []
        for context in root.findall('context'):
            for name in context.findall('name'):
                list.append(name.text)
        # gets the last context from a file 
        for i,element in enumerate(list):
            if (i==len(list)-1):
                lastElement = element
        # process the first line (head) separately, then use head-tail iterator pattern
        # to process the rest of the messages with a "leading" comma 
        # (comma actually trails the previous line, but ensures no trailing comma at the end)
        for srcContext in root.findall('context'):
            head_tail_iter = iter( srcContext.findall('message') )
            writeJSONEntry( next(head_tail_iter), destFile, srcContext, srcFile)
            for srcMessage in head_tail_iter:
                destFile.write(",")
                writeJSONEntry( srcMessage, destFile, srcContext, srcFile)
            # checks if context name is same as the last context 
            # Add comma if its not the last context of a file
            for contextName in srcContext.findall('name'):
                if(contextName.text != lastElement):
                    destFile.write(",")
        destFile.write("\n}\n"); # close file with curly brace
