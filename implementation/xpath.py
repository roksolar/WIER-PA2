# Import libraries
from lxml import html
import re
import json
from bs4 import BeautifulSoup


# We rather use the locally-cached file as it may have changed online.
pageContent = open('../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html', 'r').read()
#print("Page content:\n'%s'." % pageContent)

dataItem = {
        "Title": "",
        "Subtitle": "",
        "Author": "",
        "Time": "",
        "Lead": "",
        "Content": ""
    }

# Form an XML tree using lxml library
tree = html.fromstring(pageContent)
title = str(tree.xpath('//header[@class="article-header"]/h1/text()'))
dataItem["Title"] = title

subtitle = str(tree.xpath('//div[@class="subtitle"]/text()'))
dataItem["Subtitle"] = subtitle

author = str(tree.xpath('//div[@class="author-timestamp"]/strong/text()'))
dataItem["Author"] = author

time = str(tree.xpath('//div[@class="author-timestamp"]/text()[2]'))
dataItem["Time"] = time

lead = str(tree.xpath('//p[@class="lead"]/text()'))
dataItem["Lead"] = lead

content = str(tree.xpath(' .//article[@class="article"]/p//text()'))
dataItem["Content"] = content

print("Output object:\n%s" % json.dumps(dataItem, indent=4, ensure_ascii=False))

#OVERSTOCK WEBSITE
pageContent = open('../input/overstock.com/jewelry02.html', 'r').read()
#print("Page content:\n'%s'." % pageContent)

# Form an XML tree using lxml library
tree = html.fromstring(pageContent)

title = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/a/b/text()'))
extracted = []

regex = r"'(.*?)'|\"(.*?)\""


matches = re.finditer(regex, title)

for tit in matches:
    dataItem = {
        "Title": "",
        "Content": "",
        "ListPrice": "",
        "Price": "",
        "Saving": "",
        "SavingPercent": ""
    }
    dataItem["Title"] = tit.group(1)
    extracted.append(dataItem)

listPrice = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()'))
i = 0

regex = r"'(\$.*?)'"
matches = re.finditer(regex, listPrice)
for tit in matches:
    extracted[i]["ListPrice"] = tit.group(1)
    i = i + 1

price = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()'))


i = 0

regex = r"'(\$.*?)'"
matches = re.finditer(regex, price)
for tit in matches:
    extracted[i]["Price"] = tit.group(1)
    i = i + 1


saving = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()'))

regex = r"(\$.*?) \((.*?\d{1,3}%)\)"

matches = re.finditer(regex, saving)

i = 0
for match in matches:
    extracted[i]["Saving"] = match.group(1)
    extracted[i]["SavingPercent"] = match.group(2)
    i += 1

content = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[2]/span/text()'))

regex = r"'(.*?)'|\"(.*?)\""

matches = re.finditer(regex, content)

i = 0
for tit in matches:
    extracted[i]["Content"] = tit.group(1)
    i = i + 1

#print("Output object:\n%s" % json.dumps(extracted, indent=4, ensure_ascii=False))
