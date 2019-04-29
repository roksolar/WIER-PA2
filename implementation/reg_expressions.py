import re
import json
from bs4 import BeautifulSoup


def extract_overstock(html):
    extracted = []
    # TITLE
    regex = r"<td valign=\"top\">[\s\S]*?<a href=\"(.*)\"><b>(.*)</b></a>"
    matches = re.finditer(regex, html)
    for match in matches:
        dataItem = {
            "Title": "",
            "Content": "",
            "ListPrice": "",
            "Price": "",
            "Saving": "",
            "SavingPercent": ""
        }
        title = match.group(2)
        dataItem["Title"] = title
        extracted.append(dataItem)

    # CONTENT
    regex = r"<td valign=\"top\">[\s\S]*?<span class=\"normal\">([\s\S]*?)<br><a href=\".*><span class=\"tiny\"><b>(.*)<\/b>"
    matches = re.finditer(regex, html)
    i = 0
    for match in matches:
        extracted[i]["Content"] = match.group(1) + " " + match.group(2)
        i += 1


    # LIST PRICE
    regex = r"<s>(.*)<\/s>"
    matches = re.finditer(regex, html)
    i = 0
    for match in matches:
        extracted[i]["ListPrice"] = match.group(1)
        i += 1


    # PRICE
    regex = r"<span class=\"bigred\"><b>(.*)</b></span>"
    matches = re.finditer(regex, html)
    i = 0
    for match in matches:
        extracted[i]["Price"] = match.group(1)
        i += 1

    # SAVING & SAVING PERCENT
    regex = r"<span class=\"littleorange\">(\$.*?) \((.*?\d{1,3}%)\)</span>"
    matches = re.finditer(regex, html)
    i = 0
    for match in matches:
        extracted[i]["Saving"] = match.group(1)
        extracted[i]["SavingPercent"] = match.group(2)
        i += 1
    print("Output object:\n%s" % json.dumps(extracted, indent=4, ensure_ascii=False))


def extract_rtv(html):

    # AUTHOR & TIME
    regex = r"<div class=\"author-timestamp\">\s*<strong>(.*)\s*<\/strong>\|\s*(\w*. \w* \w* \w* \w*:\w*)"
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
    regex = r"(?=(?:<\/figure><p>|<\/p><p( class=\"Body\")?>)(?!<iframe)(.+?)?<\/p>)|<span class=\"icon-photo\"></span>(.*)</figcaption>"
    matches = re.finditer(regex, html)
    content = ""
    for match in matches:
        if match.group(3) is not None:
            content += match.group(3)
        if match.group(2) is not None:
            content += match.group(2)

    # Remove extra html tags (<br>, <strong>, etc)
    clean_content = BeautifulSoup(content, "lxml").text
    dataItem = {
        "Autor": author,
        "PublishedTime": published_time,
        "Title": title,
        "SubTitle": subtitle,
        "Lead": lead,
        "Content": clean_content
    }

    print("Output object:\n%s" % json.dumps(dataItem, indent = 4, ensure_ascii=False))


def extract_podnapisi(html):
    print("TODO")

print("RTVSLO 1: Audi A6 50 TDI quattro_ nemir v premijskem razredu")
html = open('../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html','r', encoding='utf-8').read()
extract_rtv(html)
print("--------------------------------------------------------------")
print("RTVSLO 2: Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si")
html = open('../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html','r', encoding='utf-8').read()
extract_rtv(html)
print("--------------------------------------------------------------")
print("JEWELRY 1")
html = open('../input/overstock.com/jewelry01.html','r').read()
extract_overstock(html)
print("--------------------------------------------------------------")
print("JEWELRY 2")
html = open('../input/overstock.com/jewelry02.html','r').read()
extract_overstock(html)
print("--------------------------------------------------------------")
print("PODNAPISI 1")
html = open('../input/podnapisi.net/Searching for subtitles.html','r').read()
extract_podnapisi(html)
print("--------------------------------------------------------------")
print("PODNAPISI 2")
html = open('../input/podnapisi.net/Searching for subtitles2.html','r').read()
extract_podnapisi(html)
print("--------------------------------------------------------------")