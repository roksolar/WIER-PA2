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
        wrapper.append("</" + tag + ">")
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
        sample.append("</" + tag + ">")
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

    def get_possbile_square_location(self, count, in_list):
        start = 0
        for i in range(count, 0, -1):
            if "<li" in in_list[i]:
                start = i
                break
        for i in range(count, len(in_list)):
            if in_list[i] == "</li>":
                return start, i
            if in_list[i] == "</ul>":
                return None

    def get_possbile_square_locationN(self, count, in_list):
        start = 0
        list = []
        for i in range(count, 0, -1):
            if "</" in in_list[i]:
                list.append(in_list[i])

        for i in range(count, len(in_list)):
            if in_list[i] == "</li>":
                return start, i
            if in_list[i] == "</ul>":
                return None

    def try_square_matching(self, pot_square, in_list):
        square = []
        start = pot_square[0]
        finish = pot_square[1]
        diff = (finish - start) + 1
        for i in range(finish, start -1, -1):
            if "<" not in in_list[i] and "<" not in in_list[i-diff]:
                if in_list[i] == in_list[i-diff]:
                    square.append(in_list[i])
                else:
                    square.append("#PCDATA")
                continue
            if in_list[i] != in_list[i-diff]:
                return False, ""
            else:
                square.append(in_list[i])
        square.reverse()
        return True, "".join(square)

    def fix_wrapper(self, square):
        for i in range(len(generated_wrapper)-1, 0, -1):
            if "<ul>" != generated_wrapper[i]:
                del generated_wrapper[-1]
            else:
                break
        generated_wrapper.append("( "+square+" )+")


    def find_ul_square(self, count, in_list):
        ul_start = 0
        ul_finish = 0
        for i in range(count, 0, -1):
            if "<ul>" == in_list[i]:
                ul_start = i
                break
        for i in range(count, len(in_list)):
            if "</ul>" == in_list[i]:
                ul_finish = i
                break
        return ul_start, ul_finish

    def get_open_tag(self,count, in_list ):
        tags = []
        i = count
        if "/>" in in_list[i] or "</" in in_list[i]:
            return None
        while True:
            if "</" in in_list[i]:
                tags.pop()
            elif "<" in in_list[i]:
                tags.append(in_list[i])
            if len(tags)==0:
                return (count , i)
            i = i+1

    def is_it_repeating(self, pot_square, in_list):
        start = pot_square[0]
        finish = pot_square[1]
        diff = (finish - start) + 1
        for i in range(finish, start - 1, -1):
            if "<" not in in_list[i] or "<" not in in_list[i-diff]:
                continue
            if in_list[i] == in_list[i-diff]:
                continue
            elif i in optional or (i-diff) in optional:
                continue
            else :
                return False
        return True


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

#print(wrapper)

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

#print(sample)
#-------------------------------------------

# TODO: generate wrapper

wrapper_count = 0
sample_count = 0
generated_wrapper = []
matching = MatchingMethods()
optional = []

while True:
    if sample_count==len(sample) or wrapper_count==len(wrapper):
        break
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
        else:       # tag mismatch
            s1_square = MatchingMethods.get_open_tag(MatchingMethods, sample_count, sample)
            w2_square = MatchingMethods.get_open_tag(MatchingMethods, wrapper_count, wrapper)
            if s1_square != None:
                if MatchingMethods.is_it_repeating(MatchingMethods, s1_square, sample):
                    a = 10
                else:
                    mismatch = MatchingMethods.get_tag_mismatch(MatchingMethods, sample_count, sample)
                    for i in range(sample_count, sample_count + mismatch.counter + 1):
                        optional.append(i)
                    sample_count += mismatch.counter
                    generated_wrapper.append(mismatch.string)
            elif w2_square != None:
                if MatchingMethods.is_it_repeating(MatchingMethods, w2_square, wrapper):
                    a = 10
                else:
                    mismatch = MatchingMethods.get_tag_mismatch(MatchingMethods, sample_count, sample)
                    for i in range(sample_count, sample_count + mismatch.counter + 1):
                        optional.append(i)
                    sample_count += mismatch.counter
                    generated_wrapper.append(mismatch.string)
            else:
                mismatch = MatchingMethods.get_tag_mismatch(MatchingMethods, sample_count, sample)
                for i in range(sample_count, sample_count + mismatch.counter + 1):
                    optional.append(i)
                sample_count += mismatch.counter
                generated_wrapper.append(mismatch.string)
print(generated_wrapper)
