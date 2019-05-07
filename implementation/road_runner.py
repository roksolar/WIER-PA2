from lxml import etree
from html.parser import HTMLParser
import io
import sys
from bs4 import BeautifulSoup

path_to_page1 = '../input/overstock.com/overstock_working1.html'
path_to_page2 = '../input/overstock.com/overstock_working2.html'
#path_to_page1 = '../input/partis.si/partis_working1.html'
#path_to_page2 = '../input/partis.si/partis_working2.html'

class Element:
  is_square_start = False
  is_square_end = False
  is_optional = False
  def __init__(self, name, attrs, is_tag, is_end_tag):
    self.name = name
    self.attrs = attrs
    self.is_tag = is_tag
    self.is_end_tag = is_end_tag

  def __str__(self):
      if self.is_optional:
          return "(" + self.name + ")?"
      elif self.is_square_start:
          return "(" + self.name
      elif self.is_square_end:
          return self.name + ")+"
      else:
          return self.name

  def set_square_start(self):
      self.is_square_start = True

  def set_square_end(self):
      self.is_square_end = True

  def set_is_optional(self):
      self.is_optional = True


class MyHTMLParser1(HTMLParser):

    def handle_starttag(self, tag, attrs):
        wrapper.append(Element("<"+ tag+ ">", attrs, True, False))

    def handle_endtag(self, tag):
        wrapper.append(Element("</" + tag + ">", None, True, True))

    def handle_data(self, data):
        if data.strip() != '':
            wrapper.append(Element(data, None, False, False))


class MyHTMLParser2(HTMLParser):
    def handle_starttag(self, tag, attrs):
        sample.append(Element("<"+ tag+ ">", attrs, True, False))

    def handle_endtag(self, tag):
        sample.append(Element("</" + tag + ">", None, True, True))

    def handle_data(self, data):
        if data.strip() != '':
            sample.append(Element(data, None, False, False))


parser = etree.HTMLParser()

# --------------------------------------
# Read first page
#with open('../input/overstock.com/jewelry01.html', 'r') as file:
#    data = file.read()

with open(path_to_page1, 'r') as file:
    data = file.read()


#XHTML
tree = etree.parse(io.StringIO(data), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
# Remove \n \t \r
soup = BeautifulSoup(result.decode("utf-8").replace('\n', '').replace('\t', '').replace('\r', ''), 'lxml')
# Remove script tags
[s.extract() for s in soup('script')]
# Only use body
soup = [s.extract() for s in soup('body')]
wrapper = []  # Page 1 = initial wrapper
# Generate list of tokens for page 1
parser = MyHTMLParser1()
parser.feed(str(soup[0]))

# --------------------------------------
# Read second page
#with open('../input/overstock.com/jewelry02.html', 'r') as file:
#    data = file.read()

with open(path_to_page2, 'r') as file:
    data = file.read()

#XHTML
parser = etree.HTMLParser()
tree = etree.parse(io.StringIO(data), parser)
result = etree.tostring(tree.getroot(), pretty_print=True, method="html")
# Remove \n \t \r
soup = BeautifulSoup(result.decode("utf-8").replace('\n', '').replace('\t', '').replace('\r', ''), 'lxml')
# Remove script tags
[s.extract() for s in soup('script')]
# Only use body
soup = [s.extract() for s in soup('body')]
sample = []  # Page 1 = initial wrapper
# Generate list of tokens for page 1
parser = MyHTMLParser2()
parser.feed(str(soup[0]))


def find_square(page1, page2, page1_count, page2_count):

    terminal_tag = page1[page1_count - 1]
    next_terminal_tag_index = page1_count + 1
    # Looking for future terminal tag on PAGE 1
    i = page1_count + 1
    for ele_page2 in page1[page1_count + 1:len(page1)]:
        redo = False
        if ele_page2.name == terminal_tag.name:
            # Found terminal tag. Backtrack
            square = []
            for ele_page2, ele2 in zip(page1[next_terminal_tag_index:page1_count - 1:-1],
                                 page1[page1_count - 1:0:-1]):
                if redo:
                    break
                if not ele_page2.is_tag and not ele2.is_tag and ele_page2.name != ele2.name:
                    square.append(Element("#PCDATA", None, False, False))
                else:
                    square.append(ele_page2)
                if ele_page2.name != ele2.name and (ele_page2.is_tag or ele2.is_tag):
                    redo = True
                    continue
            if redo:
                next_terminal_tag_index += 1
                continue

            if len(square) > 0:
                square[0].set_square_end()
                square[len(square) - 1].set_square_start()

            # Found repetition further on PAGE1. Find same repetitions back from missmatch on wrapper

            ele_page2 = page2[page2_count - 1]

            index_page2 = page2_count - 1
            ele_square = square[0]
            square_index = 0
            found_one = False

            while ele_page2.name == ele_square.name or (not ele_page2.is_tag and not ele_square.is_tag):
                if square_index > len(square):
                    found_one = True
                index_page2 -= 1
                ele_page2 = page2[index_page2]
                square_index += 1
                i = square_index % (len(square))
                ele_square = square[i]
            if found_one:
                return [index_page2 +1+i , page2_count - 1, square]

            else:
                next_terminal_tag_index += 1
                continue
        next_terminal_tag_index += 1
    return [-1, -1, None]


def locate_further_squares(page, sample_count, square):

    square = list(reversed(square))
    index_page = sample_count
    index_square = 0
    ele_page = page[index_page]
    ele_square = square[index_square]
    found_one = False
    while ele_page.name == ele_square.name or (not ele_page.is_tag and not ele_square.is_tag):
        if index_square == len(square) - 1:
            found_one = True
        index_page += 1
        index_square += 1
        ele_page = page[index_page]
        i = index_square % (len(square))
        ele_square = square[i]
    if found_one:
        return index_page
    else:
        return sample_count


def try_find_iterator(sample, wrapper, sample_count, wrapper_count):
    # Terminal tags must match
    if sample[sample_count - 1].name != wrapper[wrapper_count - 1].name:
        return [wrapper_count, sample_count, wrapper, False]
    # Terminal tags match. Try finding squares
    [start, end, square] = find_square(sample, wrapper, sample_count, wrapper_count)

    if start != -1 and end != -1:
        sample_count = locate_further_squares(sample, sample_count, square)
        wrapper = change_wrapper(wrapper, start, end+1, list(reversed(square)), "ROK1")
        return [wrapper_count, sample_count, wrapper, True]

    else:
        #[start, end, square] = find_square(wrapper, sample, wrapper_count, sample_count)
        [start, end, square] = find_square(wrapper, wrapper, wrapper_count, wrapper_count)
    if start == -1 and end == -1:
        return [wrapper_count, sample_count, wrapper, False]
    # Edit wrapper
    wrapper_count = locate_further_squares(wrapper, wrapper_count, square)
    wrapper = change_wrapper(wrapper, start, wrapper_count, list(reversed(square)), "ROK2")
    return [wrapper_count, sample_count, wrapper, True]


def try_find_optional(wrapper_count,sample_count,sample,wrapper):
    wrapper_tag = wrapper[wrapper_count].name
    sample_tag = sample[sample_count].name
    sample_object = sample[sample_count]
    #cross matching
    max = 999999999999999
    #try to find tag from sample in wrapper
    index_of_tag_in_wrapper = max
    for i in range(wrapper_count,(wrapper_count+10000)):
        if i >= len(wrapper):
            break
        if(wrapper[i].name == sample_tag):
            index_of_tag_in_wrapper = i-wrapper_count
            wrapper[wrapper_count].set_is_optional()
            wrapper_count = wrapper_count + 1

            return [wrapper_count, sample_count, wrapper]

    index_of_tag_in_sample = max
    if(index_of_tag_in_wrapper == max):
        # try to find tag from wrapper in sample
        index_of_tag_in_sample = max
        for i in range(sample_count, len(sample)):
            if(sample[i].name == wrapper_tag):
                sample_object.set_is_optional()
                wrapper.insert(wrapper_count,sample_object)
                wrapper_count = wrapper_count + 1
                sample_count = sample_count + 1
                return [wrapper_count, sample_count, wrapper]


def change_wrapper(wrapper,start,end,content, source):
    try:
        for i in range(end-start):
            del wrapper[start]

        while start != end-len(content):
            wrapper.insert(start,None)
            start = start + 1

        for el in content:
            wrapper.insert(start,el)
            start = start + 1

    except Exception as e:
        print(source)
        print(e)
        sys.exit("Error message")

    return wrapper


wrapper_count = 0
sample_count = 0
generated_wrapper = []
while True:
    if sample_count==len(sample) or wrapper_count==len(wrapper):
        break

    sample_ele = sample[sample_count]
    wrapper_ele = wrapper[wrapper_count]

    if sample_ele.name == wrapper_ele.name:
        wrapper_count += 1
        sample_count += 1
        continue

    elif sample_ele.name != wrapper_ele.name and not sample_ele.is_tag and not wrapper_ele.is_tag:
        wrapper[wrapper_count] = Element("#PCDATA", None, False, False)
        wrapper_count += 1
        sample_count += 1
        continue

    else:
        [wrapper_count, sample_count, wrapper, success] = try_find_iterator(sample, wrapper, sample_count, wrapper_count)
        if not success:
            [wrapper_count, sample_count, wrapper] = try_find_optional(wrapper_count, sample_count, sample, wrapper)

print("-------------- WRAPPER -----------------")
html = ""
for el in wrapper:
    if el is not None:
        print(el)
