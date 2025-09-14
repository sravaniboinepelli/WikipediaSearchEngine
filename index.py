import sys
from lxml import etree
from parse import Parser
from tools import Tokenizer
from tools import StopWordStem
from tools import Indexer
from sort import sort_file
from compressor import index_compressor, si_creator

prefix = 'http://www.mediawiki.org/xml/export-0.10/'

doc_dict = {}

# WikiIndexCreator class
class WikiIndexCreator:
    # Initialize with all natural language tools
    def __init__(self):
        self.parser = Parser(prefix)
        self.tokenizer = Tokenizer()
        self.sws = StopWordStem()
        self.indexer = Indexer()

    # Method to process text
    def process(self, text):
        # Tokenize the text
        text = self.tokenizer.tokenize(text)
        # Remove stop words and stem using porter stemmer
        text = self.sws.remove_and_stem(text)
        # Create the counter dictionary
        text = self.indexer.create_map(text)
        return text

    # Method to obtain the fields
    def build_params(self, element):
        # Parse the page
        id, title, body, cat, info, links, refs = self.parser.parse_page(element)
        doc_dict[id] = title

        # Process each field
        title = self.process(title)
        body = self.process(body)
        cat = self.process(cat)
        info = self.process(info)
        links = self.process(links)
        refs = self.process(refs)

        # Obtain combined index
        index = self.indexer.combine_maps(title, body, cat, info, links, refs)
        return index, id

    # Method to create the inverted index
    def create(self, infilename, outfilename):
        # Obtain page using lxml
        context = etree.iterparse(infilename, events=('end',), tag='{'+prefix+'}page')

        out = open("temp", 'w+')
        # Iterate through each page element
        for event, elem in context:
            # Obtain the index and ids
            index, id = self.build_params(elem)

            # Putting the words into the array
            for word in index:
                line = word + ":" + "d" + id + "-"
                if "t" in index[word]:
                    line += "t" + str(index[word]["t"])
                if "b" in index[word]:
                    line += "b" + str(index[word]["b"])
                if "c" in index[word]:
                    line += "c" + str(index[word]["c"])
                if "i" in index[word]:
                    line += "i" + str(index[word]["i"])
                if "l" in index[word]:
                    line += "l" + str(index[word]["l"])
                if "r" in index[word]:
                    line += "r" + str(index[word]["r"])
                out.write(line + "\n")

            # To quicken the process
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]

        out.close()

        # In case the index is very big
        sort_file("temp", "1G")

        # Compress index by using gaps
        index_compressor("temp.out", outfilename)

        # Break index file and make secondary index
        si_creator(outfilename)


# Obtain and provide the args
length = len(sys.argv)
if length < 3:
    print("Not enough arguments given. Please specify input and output files.")
else:
    indexer = WikiIndexCreator()
    indexer.create(sys.argv[1], sys.argv[2]+"index.txt")
    map_file = open(sys.argv[2] + "mapping.txt", 'w+')
    for key in doc_dict:
        map_file.write(str(key)+" "+str(doc_dict[key])+"\n")
