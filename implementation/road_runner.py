from lxml import etree
from html.parser import HTMLParser
import collections
import io

class MyHTMLParser1(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # TODO: kaj z atributi?
        if len(attrs) == 0:
            wrapper.append("<"+ tag+ ">")
        else:
            wrapper.append("<" + tag + str(attrs).strip('[]()') + ">")
        #print("Encountered a start tag: <"+ tag+ ">")

    def handle_endtag(self, tag):
        wrapper.append("<" + tag + "/>")
        #print("Encountered an end tag : </"+ tag+ ">")

    def handle_data(self, data):
        wrapper.append(data)
        #print("Encountered some data  :"+ data)

class MyHTMLParser2(HTMLParser):
    def handle_starttag(self, tag, attrs):
        #TODO: kaj z atributi?
        if len(attrs) == 0:
            sample.append("<"+ tag+ ">")
        else:
            sample.append("<" + tag + str(attrs).strip('[]()').replace("'", "") + ">")
        #print("Encountered a start tag: <"+ tag+ ">")

    def handle_endtag(self, tag):
        sample.append("<" + tag + "/>")
        #print("Encountered an end tag : </"+ tag+ ">")

    def handle_data(self, data):
        sample.append(data)
        #print("Encountered some data  :"+ data)


class MatchingMethods:

    def both_string(self, w_ele, s_ele):
        return "<" not in w_ele and "<" not in s_ele

    def get_tag_mismatch(self, count, s_list):
        Mismatch = collections.namedtuple('Point', ['string', 'counter'])
        optional = ""
        start_mis = s_list[count]
        end_mis = start_mis.replace(">", "/>")
        if "/>" in s_list[count]:
            return Mismatch(string="( "+ start_mis +" )?" , counter=1)
        else:
            counter = 0
            while True:
                optional += s_list[count] +" "
                counter += 1
                if end_mis == s_list[count]:
                    return Mismatch(string="( "+ optional +" )?", counter=counter)

    def find_square(self, w_list, s_list):
        ul_w = [i for i, x in enumerate(w_list) if x == "<ul>"]
        ul_s = [i for i, x in enumerate(s_list) if x == "</ul>"]
        ul_end_w = [i for i, x in enumerate(w_list) if x == "<ul>"]
        ul_end_s = [i for i, x in enumerate(s_list) if x == "</ul>"]



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

sample = []
# Generate list of tokens for page 2
parser = MyHTMLParser2()
parser.feed(result.decode("utf-8").replace('\n', '').replace('\t', '').replace('\r', ''))

print(sample)
#-------------------------------------------

# TODO: generate wrapper

wrapper_count = 0
sample_count = 0
generated_wrapper = []
matching = MatchingMethods()

for i in range(max(len(sample), len(wrapper))):
    sample_ele = sample[sample_count]
    wrapper_ele = wrapper[wrapper_count]
    if sample_ele == wrapper_ele:
        generated_wrapper.append(sample_ele)
        wrapper_count += 1
        sample_count += 1
        continue
    else:
        if matching.both_string(sample_ele, wrapper_ele): #string mismatch
            generated_wrapper.append("#PCDATA")
            wrapper_count += 1
            sample_count += 1
            continue
        else:       #tag mismatch
            mismatch = MatchingMethods.get_tag_mismatch(MatchingMethods, sample_count, sample)
            sample_count += mismatch.counter
            generated_wrapper.append(mismatch.string)
print(generated_wrapper)
