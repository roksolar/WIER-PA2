from lxml import etree
import io

with open('stran', 'r') as file:
    data = file.read()

parser = etree.HTMLParser()
tree = etree.parse(io.StringIO(data), parser)

result = etree.tostring(tree.getroot(), pretty_print=True, method="html") #xhtml format
list = tree.iter() #lista elementov
for a in list:
    print(a)