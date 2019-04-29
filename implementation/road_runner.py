from lxml import etree
from html.parser import HTMLParser
import io

class MyHTMLParser1(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # TODO: kaj z atributi?
        wrapper.append("<"+ tag+ ">")
        #print("Encountered a start tag: <"+ tag+ ">")

    def handle_endtag(self, tag):
        wrapper.append("<" + tag + ">")
        #print("Encountered an end tag : </"+ tag+ ">")

    def handle_data(self, data):
        wrapper.append(data)
        #print("Encountered some data  :"+ data)

class MyHTMLParser2(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #TODO: kaj z atributi?
        list_of_tokens.append("<"+ tag+ ">")
        #print("Encountered a start tag: <"+ tag+ ">")

    def handle_endtag(self, tag):
        list_of_tokens.append("<" + tag + ">")
        #print("Encountered an end tag : </"+ tag+ ">")

    def handle_data(self, data):
        list_of_tokens.append(data)
        #print("Encountered some data  :"+ data)

parser = etree.HTMLParser()

# --------------------------------------
# Read first page
with open('../input/simple_sample1.html', 'r') as file:
    data = file.read()

tree = etree.parse(io.StringIO(data), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html")  #xhtml format

wrapper = []  # Page 1 = initial wrapper
# Generate list of tokens for page 1
parser = MyHTMLParser1()
parser.feed(result.decode("utf-8").replace('\n', '').replace('\t', '').replace('\r', ''))

print(wrapper)

# --------------------------------------
# Read second page
with open('../input/simple_sample2.html', 'r') as file:
    data = file.read()
parser = etree.HTMLParser()
tree = etree.parse(io.StringIO(data), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html") #xhtml format

list_of_tokens = []
# Generate list of tokens for page 2
parser = MyHTMLParser2()
parser.feed(result.decode("utf-8").replace('\n', '').replace('\t', '').replace('\r', ''))

print(list_of_tokens)
#-------------------------------------------

# TODO: generate wrapper

