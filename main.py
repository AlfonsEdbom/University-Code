import nltk
from xml.dom import minidom

dom = minidom.parse("train.xml")

for qtag in dom.getElementsByTagName("utterance"):
    if qtag.getAttribute("sensical") == "true":
        print(f"{qtag.getAttribute('text')} makes sense")
    else:
        print(f"{qtag.getAttribute('text')} is weird")