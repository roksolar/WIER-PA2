# Import libraries
from lxml import html

# Define the XML document
xmlDocument = """
          <?xml version="1.0" encoding="UTF-8"?>

          <bookstore>

          <book category="cooking">
            <title lang="en">Everyday Italian</title>
            <author>Giada De Laurentiis</author>
            <year>2005</year>
            <price>30.00</price>
          </book>

          <book category="children">
            <title lang="en">Harry Potter</title>
            <author>J K. Rowling</author>
            <year>2005</year>
            <price>29.99</price>
          </book>

          <book category="web">
            <title lang="en">XQuery Kick Start</title>
            <author>James McGovern</author>
            <author>Per Bothner</author>
            <author>Kurt Cagle</author>
            <author>James Linn</author>
            <author>Vaidyanathan Nagarajan</author>
            <year>2003</year>
            <price>49.99</price>
          </book>

          <book category="web">
            <title lang="en">Learning XML</title>
            <author>Erik T. Ray</author>
            <year>2003</year>
            <price>39.95</price>
          </book>

          </bookstore>
"""

# Form an XML tree using lxml library
tree = html.fromstring(xmlDocument)

# Select all titles (the result will be a list of lxml Element objects)
tree.xpath('//title')

# Select the first element from the above query and retrieve text data from it
tree.xpath('//title')[0].text

# Similar to the above but getting title texts directly using XPath
tree.xpath('//title/text()')

# More explicit version of the above
tree.xpath('//bookstore/book/title/text()')

# Select first authors only
tree.xpath('//bookstore/book/author[1]/text()')

# Select titles of english books that are cheaper than 30 EUR
tree.xpath('//bookstore/book[price<30]/title[@lang="en"]/text()')

###################
# We rather use the locally-cached file as it may have changed online.
pageContent = open('Golf8.html', 'r').read()
print("Page content:\n'%s'." % pageContent)


# Form an XML tree using lxml library
tree = html.fromstring(pageContent)

# Get the article title
title = str(tree.xpath('//*[@id="container"]/div//h1/text()')[0])
print("Found title: '%s'." % title)

# Get the date (cannot handle text directly using XPath)
date = str(tree.xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[1]/text()')[0])
print("Found date: '%s'." % date)

# Additionally format date
date = re.sub(r"\s", "", date)
print("Found date: '%s'." % date)

# Extract the image URL
imageUrl = str(tree.xpath('//*[@id="container"]/div/div[1]/div[1]/div[1]/div/div[2]/a/img/@src')[0])
print("Found imageUrl: '%s'." % imageUrl)

# Form and output JSON
import json

dataItem = {
    "title": title,
    "date": date,
    "imageUrl": imageUrl
}

print("Output object:\n%s" % json.dumps(dataItem, indent = 4))