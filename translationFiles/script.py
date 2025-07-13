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
global stringSearchable
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

def cleanupNewLine(elem, level=0):
    if len(elem):
        for subelem in elem:
            stringgg = subelem.text
            if(subelem.text != None):
                if(subelem.text.find("\\n") != -1):
                    loc = subelem.text.find("\\n")
                    subelem.text = subelem.text.replace("\\n", "\x0a")
            cleanupNewLine(subelem, level+1)
    return elem

# adds new <context> tag with <name> tag inside it
def add_context(fileRoot,fileName):
    #creates subelement of root node
    newContext = ET.SubElement(fileRoot, "context")
    #adds file name in <name> tag
    contextName = ET.SubElement(newContext, "name").text = fileName
    return newContext

# adds new message
def add_message(context, stringName, stringComment, pageLink, userLevel, stringSearchable):
    # checks for the string existence and removes if same string in the same context already exists
    check_message_exists(context, stringName)
    #creates message as child node of context and add child nodes to the message
    message = ET.SubElement(context, "message")
    ET.SubElement(message, "source").text = stringName
    ET.SubElement(message, "comment").text = stringComment
    ET.SubElement(message, "extracomment").text = userLevel +"-" + pageLink + "-" + stringSearchable
    ET.SubElement(message, "translation", type="unfinished").text = ' '


def check_message_exists(context, stringVar):
    for srcMessage in context.findall('message'):
        if  (srcMessage is not None) and(srcMessage.find('source').text == stringVar):
            # matching message found, so remove the existing one
            context.remove( srcMessage )


def appendFiles(tsFileName):
    scriptFile = ET.parse(tsFileName)
    scriptFileRoot = scriptFile.getroot()
    folderPath = '../../../app'
    pattern = "*.ts"
    # read all the directories and sub-directories from the specified folder
    for path, subdirs, files in os.walk(folderPath):
        for name in files:
            # checks for the .ts files
            if fnmatch(name, pattern):
                # used this flag to create the context only once for each file
                firstTime = True
                # opens read the file with read permission
                with open(os.path.join(path, name), 'r', encoding='utf-8') as file:
                    for line in file:
                        # checks if line starts with 'const STRING_'
                        if line.startswith('const STRING_'):
                            #print(line)
                            # stores the page link, user name, string and comment in variables
                            if ('PAGE_LINK' in line):
                                pageLink = line.split("'",2)[1]
                            elif 'USER_LEVEL' in line:
                                userLevel = line.split("'",2)[1]
                            else:
                                stringNameArray = line.split("=",1)[1]
                                stringName = stringNameArray.split("'")[1]
                                stringComment = stringNameArray.split("'")[3]
                                if (len(stringNameArray.split("'")) > 5):
                                    stringSearchable = stringNameArray.split("'")[5]
                                else:
                                    stringSearchable = ""
                                # used this flag to check if message is already added in the context
                                messageAdded = False
                                # checks if context is already there
                                if (scriptFileRoot.findall('context') != []):
                                    # file has exisiting context, checks for the same context name against file name
                                    for srcContext in scriptFileRoot.findall('context'):
                                        if (srcContext.find('name').text == name):
                                            #file has exisiting context and is same as the current file name
                                            # Adds message to the existing context
                                            add_message(srcContext, stringName, stringComment, pageLink, userLevel, stringSearchable)
                                            messageAdded = True
                                    # file has exisiting context, checks for the same context name against file name
                                    if not messageAdded:
                                        if firstTime:
                                            newContext = add_context(scriptFileRoot, name)
                                            firstTime = False
                                        add_message(newContext,stringName, stringComment, pageLink, userLevel, stringSearchable)
                                else:
                                    # file doesn't have any context tag and add new context
                                    if firstTime:
                                        newContext = add_context(scriptFileRoot, name)
                                        firstTime = False
                                    add_message(newContext,stringName, stringComment, pageLink, userLevel, stringSearchable)
    print("appended " + tsFileName)
    scriptFile = ET.ElementTree(cleanupNewLine(indent(scriptFileRoot)))
    scriptFile.write(tsFileName, xml_declaration=True, encoding='utf-8')



appendFiles('FO.ts')
appendFiles('EN.ts')
appendFiles('DE.ts')
appendFiles('ES.ts')
appendFiles('FR.ts')
appendFiles('IT.ts')
appendFiles('JA.ts')
appendFiles('KO.ts')
appendFiles('PL.ts')
appendFiles('PT.ts')
appendFiles('RU.ts')
appendFiles('ZH.ts')
