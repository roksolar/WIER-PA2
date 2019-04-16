# Import libraries
from lxml import html

# We rather use the locally-cached file as it may have changed online.
pageContent = open('../input/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html', 'r').read()
#print("Page content:\n'%s'." % pageContent)

# Form an XML tree using lxml library
tree = html.fromstring(pageContent)
title = str(tree.xpath('//header[@class="article-header"]/h1/text()'))
print("Found title: '%s'." % title)

subtitle = str(tree.xpath('//div[@class="subtitle"]/text()'))
print("Found subtitle: '%s'." % subtitle)

author = str(tree.xpath('//div[@class="author-timestamp"]/strong/text()'))
print("Found author: '%s'." % author)

time = str(tree.xpath('//div[@class="author-timestamp"]/text()[2]'))
print("Found time: '%s'." % time)

lead = str(tree.xpath('//p[@class="lead"]/text()'))
print("Found lead: '%s'." % lead)

content = str(tree.xpath(' .//article[@class="article"]/p//text()'))
print("Found content: '%s'." % content)

