from xml.dom import minidom

def get_data(filename):
    text = []
    labels = []
    dom = minidom.parse(filename)
    for qtag in dom.getElementsByTagName("utterance"):
        text.append(qtag.getAttribute('text'))
        if qtag.getAttribute("sensical") == "true":
            labels.append(1)
        else:
            labels.append(0)

    return text, labels