import nltk
from xml.dom import minidom

dom = minidom.parse("examples.xml")

for qtag in dom.getElementsByTagName("question"):
    print(qtag.getAttribute("text"))
