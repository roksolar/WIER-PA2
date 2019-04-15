import re
import json

def extract_overstock(html):
    print("todo")
    #regex = r"<article class=\"article\">([\s\S]*)<\/article>"
    #match = re.compile(regex, re.UNICODE).search(html)
    #content = match.group(1)


    #dataItem = {
    #    "Title": title,
    #    "Content": content,
    #    "ListPrice": list_price,
    #    "Price": price,
    #    "Saving": saving,
    #    "SavingPercent": saving_percent
    #}

    #print("Output object:\n%s" % json.dumps(dataItem, indent = 4))

def extract_rtv(html):
    # AUTHOR & TIME
    #regex = r"<div class=\"author-timestamp\">\s*<strong>(.*)\s*<\/strong>\|\s*(.*)\s*<\/div>"
    regex = r"<div class=\"author-timestamp\">\s*<strong>(.*)\s*<\/strong>\|\s*(\w*. \w* \w* \w* \w*:\w*)"
    # regex = r"<div class=\"author-name\">\s*(\w* \w*)\s*<\/div>"
    # regex = r"<div class=\"author-name\">\s*(.*)\s*<\/div>\s*<\/div>"
    match = re.compile(regex, re.UNICODE).search(html)
    author = match.group(1)
    published_time = match.group(2)

    # TITLE
    regex = r"<h1>(.*)<\/h1>"
    match = re.compile(regex, re.UNICODE).search(html)
    title = match.group(1)

    # SUBTITLE
    regex = r"<div class=\"subtitle\">(.*)<\/div>"
    match = re.compile(regex, re.UNICODE).search(html)
    subtitle = match.group(1)

    # LEAD
    regex = r"<p class=\"lead\">(.*)<\/p>"
    match = re.compile(regex, re.UNICODE).search(html)
    lead = match.group(1)

    # CONTENT
    regex = r"<article class=\"article\">([\s\S]*)<\/article>"
    match = re.compile(regex, re.UNICODE).search(html)
    content = match.group(1)


    dataItem = {
        "Autor": author,
        "PublishedTime": published_time,
        "Title": title,
        "SubTitle": subtitle,
        "Lead": lead,
        "Content": content
    }

    print("Output object:\n%s" % json.dumps(dataItem, indent = 4))

#print("Audi A6 50 TDI quattro_ nemir v premijskem razredu")
html = open('../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html',
                   'r').read()
extract_rtv(html)

#print("Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si")
html = open('../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html',
                   'r').read()
extract_rtv(html)

html = open('../input/overstock.com/jewelry01.html',
                   'r').read()
extract_overstock(html)

html = open('../input/overstock.com/jewelry02.html',
                   'r').read()
extract_overstock(html)