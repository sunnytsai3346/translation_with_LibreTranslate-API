# Extract all the translated strings and their keys from the specified translation 
# files (*.ts), converting it to the json format used by the WebUI and writing those
# files out to the jsonDir (aka *.ts to ../src/translations/*.json).
#
# Expected format:
# <message>
#   <source>SomeKeyThatNeedsToBeTranslated</source>
#   <translation type='unfinished'>*English value to translate*</translation>
#   <comment>Context to help the tranlator</comment>
# </message>
#
# Run this (Python 3) script by opening a command window in this directory 
# (<SHIFT>+<RIGHT CLICK> + Open command window here)
# At the prompt, type:
#   python ts2json.py

import os, glob
from fnmatch import fnmatch
import xml.etree.cElementTree as ET
from operator import itemgetter


def writeJSONEntry( srcMessage, destFile, srcContextName, srcfileName):
    sourceTextString = srcMessage.find('source').text
    sourceTextKey = srcMessage.find('source').text.replace(" ", "")
    nameText = srcContextName.find('name').text.replace(".component.ts", "")
    extraComment = srcMessage.find('extracomment').text.split("-")
    translationText = srcMessage.find('translation').text.replace( '"', '\\"')
    if (srcfileName == "EN.ts"):
        destFile.write("{\n    \"" + "name" + "\": \"" + sourceTextString + "\",")
    else:
        destFile.write("{\n    \"" + "name" + "\": \"" + translationText + "\",")

    destFile.write("\n    \"" + "url" + "\": \"" + extraComment[1] + "\",")
    destFile.write("\n    \"" + "userLevel" + "\": \"" + extraComment[0] + "\"")
    destFile.write("\n}")

jsonDir = "searchFiles" + os.sep
for srcFile in glob.glob( "*.ts" ):
    tsFile = ET.parse( srcFile )
    root = tsFile.getroot()

    # build up the destination file + path
    destFileName = jsonDir + srcFile.replace('.ts', '.json')
    print( "Converting from " + srcFile + " to " + destFileName )
    with open(destFileName, 'w', encoding="utf-8") as destFile:
        destFile.write("[") # open file with curly brace
        # add all the names of contexts to a list
        list = []
        index = 0
        for tempcontext in root.findall('context'):
            for tempMessage in tempcontext.findall('message'):
                tempextraComment = tempMessage.find('extracomment').text.split("-")
                # check for the searchable strings
                if(tempextraComment[2] == "Searchable"):
                    # do not add comma for first entry
                    if(index != 0):
                        destFile.write(",\n")
                    writeJSONEntry( tempMessage, destFile, tempcontext, srcFile)
                    index += 1
        destFile.write("\n]\n")

########## commented out this code in we need it in future to add entry for all strings including serachable as well
        # for context in root.findall('context'):
        #     for name in context.findall('name'):
        #         list.append(name.text)
        # # gets the last context from a file
        # for i,element in enumerate(list):
        #     if (i==len(list)-1):
        #         lastElement = element
        #  # process the first line (head) separately, then use head-tail iterator pattern
        # # to process the rest of the messages with a "leading" comma 
        # # (comma actually trails the previous line, but ensures no trailing comma at the end)
        # for srcContext in root.findall('context'):
        #     head_tail_iter = iter( srcContext.findall('message') )
        #     writeJSONEntry( next(head_tail_iter), destFile, srcContext, srcFile)
        #     for srcMessage in head_tail_iter:
        #         destFile.write(",\n")
        #         writeJSONEntry( srcMessage, destFile, srcContext, srcFile)
        #     for contextName in srcContext.findall('name'):
        #         if(contextName.text != lastElement):
        #             destFile.write(",\n")
        # destFile.write("\n]\n"); # close file with curly brace
