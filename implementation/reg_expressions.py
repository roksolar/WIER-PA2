import re
import json

# Get the article title
#regex = r"<div class=\"col-xs-12\">\s+<h1>(.*)<\/h1>"

#match = re.compile(regex).search(pageContent)
#title = match.group(1)
#print("Found title: '%s'." % title)


#dataItem = {
#    "title": title,
#    "date": date,
#    "imageUrl": imageUrl
#}

#print("Output object:\n%s" % json.dumps(dataItem, indent = 4))

def extract_overstock1(html):
    print(html)

def extract_overstock2(html):
    print(html)

def extract_rtv1(html):
    print("Page content:\n'%s'." % html)


pageContent = open('../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html',
                   'r').read()
extract_rtv1(pageContent)