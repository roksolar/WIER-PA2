# Import libraries
from lxml import html
import re
import json
from bs4 import BeautifulSoup


def rtvslo(pageContent):
    # We rather use the locally-cached file as it may have changed online.
    #print("Page content:\n'%s'." % pageContent)

    dataItem = {
            "Title": "",
            "Subtitle": "",
            "Author": "",
            "PublishedTime": "",
            "Lead": "",
            "Content": ""
        }

    # Form an XML tree using lxml library
    tree = html.fromstring(pageContent)
    title = str(tree.xpath('//header[@class="article-header"]/h1/text()'))
    dataItem["Title"] = replace_all(title)

    subtitle = str(tree.xpath('//div[@class="subtitle"]/text()'))
    dataItem["Subtitle"] = replace_all(subtitle)

    author = str(tree.xpath('//div[@class="author-timestamp"]/strong/text()'))
    dataItem["Author"] = replace_all(author)

    time = str(tree.xpath('//div[@class="author-timestamp"]/text()[2]'))
    dataItem["PublishedTime"] = replace_all(time)

    lead = str(tree.xpath('//p[@class="lead"]/text()'))
    dataItem["Lead"] = replace_all(lead)

    content = str(tree.xpath(' .//article[@class="article"]/p//text()'))
    dataItem["Content"] = replace_all(content)

    print("Output object:\n%s" % json.dumps(dataItem, indent=4, ensure_ascii=False))

#OVERSTOCK WEBSITE
def overstock(pageContent):
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
        if(tit.group(1) is None):
            dataItem["Title"] = replace_all(tit.group(2))
        else:
            dataItem["Title"] = replace_all(tit.group(1))

        extracted.append(dataItem)

    listPrice = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td[2]/s/text()'))
    i = 0

    regex = r"'(\$.*?)'"
    matches = re.finditer(regex, listPrice)
    for tit in matches:
        extracted[i]["ListPrice"] = replace_all(tit.group(1))
        i = i + 1

    price = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/span/b/text()'))


    i = 0

    regex = r"'(\$.*?)'"
    matches = re.finditer(regex, price)
    for tit in matches:
        extracted[i]["Price"] = replace_all(tit.group(1))
        i = i + 1


    saving = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/span/text()'))

    regex = r"(\$.*?) \((.*?\d{1,3}%)\)"

    matches = re.finditer(regex, saving)

    i = 0
    for match in matches:
        extracted[i]["Saving"] = replace_all(match.group(1))
        extracted[i]["SavingPercent"] = replace_all(match.group(2))
        i += 1

    content = str(tree.xpath('.//table[@cellpadding="2"]/tbody/tr/td[2]/table/tbody/tr/td[2]/span/text()'))

    regex = r"'(.*?)'|\"(.*?)\""

    matches = re.finditer(regex, content)

    i = 0
    for tit in matches:
        if (tit.group(1) is None):
            extracted[i]["Content"] = replace_all(tit.group(2))
        else:
            extracted[i]["Content"] = replace_all(tit.group(1))

        i = i + 1

    print("Output object:\n%s" % json.dumps(extracted, indent=4, ensure_ascii=False))

def partis(pageContent):
    #print("Page content:\n'%s'." % pageContent)
    extracted = []
    # Form an XML tree using lxml library
    tree = html.fromstring(pageContent)

    naslov = str(tree.xpath('.//div[@class="list"]/div/div[2]/a/text()'))

    matches = naslov.split("',")

    for tit in matches:
        dataItem = {
            "Naslov": "",
            "Podnaslov": "",
            "Velikost": "",
            "Sejalcev": "",
            "Pijavk": "",
            "Prenosov": ""
        }
        dataItem["Naslov"] = replace_all(tit)
        extracted.append(dataItem)

    podnaslov = str(tree.xpath('.//div[@class="list"]/div/div[2]/div/div[1]/text()'))
    velikost = str(tree.xpath('.//div[@class="list"]/div/div[4]/text()'))
    sejalcev = str(tree.xpath('.//div[@class="list"]/div/div[5]/text()'))
    pijavk = str(tree.xpath('.//div[@class="list"]/div/div[6]/text()'))
    prenosov = str(tree.xpath('.//div[@class="list"]/div/div[7]/text()'))

    velikost = velikost.split("',")
    podnaslov = podnaslov.split("',")
    sejalcev = sejalcev.split("',")
    pijavk = pijavk.split("',")
    prenosov = prenosov.split("',")

    i = 0
    for match in velikost:
        extracted[i]["Podnaslov"] = replace_all(podnaslov[i])
        extracted[i]["Velikost"] = replace_all(velikost[i])
        extracted[i]["Sejalcev"] = replace_all(sejalcev[i])
        extracted[i]["Pijavk"] = replace_all(pijavk[i])
        extracted[i]["Prenosov"] = replace_all(prenosov[i])
        i += 1

    print("Output object:\n%s" % json.dumps(extracted, indent=4, ensure_ascii=False))

def replace_all(besedilo):
    return besedilo.replace(']','').replace('\n','').replace('\t','').replace('[','').replace('"','').replace("'",'').replace('|','').replace('\\t','').replace('\\n','').lstrip()


overstock_file_1 = '../input/overstock.com/jewelry01.html'
overstock_file_2 = '../input/overstock.com/jewelry02.html'
pageContent1 = open(overstock_file_1, 'r').read()
pageContent2 = open(overstock_file_2, 'r').read()

print("JEWELRY 1")
overstock(pageContent1)
print("--------------------------------------------------------------")
print("JEWELRY 2")
overstock(pageContent2)
print("--------------------------------------------------------------")

rtvslo_file_1 = '../input/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
rtvslo_file_2 = '../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html'

pageContent1 = open(rtvslo_file_1, 'r', encoding='utf-8').read()
pageContent2 = open(rtvslo_file_2, 'r', encoding='utf-8').read()

print("RTVSLO 1: Audi A6 50 TDI quattro_ nemir v premijskem razredu")
rtvslo(pageContent1)
print("--------------------------------------------------------------")
print("RTVSLO 2: Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si")
rtvslo(pageContent2)
print("--------------------------------------------------------------")

partis_file_1 = '../input/partis.si/Partis.si.html'
partis_file_2 = '../input/partis.si/Partis2.si.html'

pageContent1 = open(partis_file_1, 'r', encoding='utf-8').read()
pageContent2 = open(partis_file_2, 'r', encoding='utf-8').read()

print("PARTIS 1")
partis(pageContent1)
print("--------------------------------------------------------------")
print("PARTIS 2")
partis(pageContent2)
print("--------------------------------------------------------------")