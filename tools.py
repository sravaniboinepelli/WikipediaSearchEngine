from porter_stem import stem
from collections import Counter, defaultdict, OrderedDict
from itertools import chain

# Stop word dictionary
stop_words = {'he': 0, 'at': 0, "wont": 0, 'below': 0, "its": 0, 'under': 0,
'who': 0, 'her': 0, "wasnt": 0, 'have': 0, 'while': 0, 'how': 0, 'both': 0,
"arent": 0, 'and': 0, 'yours': 0, 'i': 0, 'in': 0, 'own': 0, "shes": 0,
'now': 0, "neednt": 0, 'few': 0, 'them': 0, 'hasn': 0, "thatll": 0,
'before': 0, 'do': 0, 'ourselves': 0, 's': 0, "youll": 0, 'himself': 0,
'same': 0, 'ain': 0, 'out': 0, 'we': 0, "hasnt": 0, 'what': 0, 'until': 0,
'herself': 0, 'needn': 0, "shant": 0, 'after': 0, "isnt": 0, 'just': 0,
'down': 0, 'doesn': 0, 'hadn': 0, 've': 0, 'more': 0, 'were': 0, 'through': 0,
'an': 0, 'can': 0, 'a': 0, "couldnt": 0, 'haven': 0, 'each': 0, 'which': 0,
'by': 0, 'wouldn': 0, 'over': 0, 'most': 0, "mightnt": 0, 'be': 0, 'off': 0,
'your': 0, "mustnt": 0, 'too': 0, 't': 0, 'hers': 0, 'its': 0, 'd': 0,
'you': 0, 'or': 0, 'is': 0, 'been': 0, 'all': 0, 'for': 0, 'if': 0,
'yourself': 0, 'had': 0, 'as': 0, 'weren': 0, 'their': 0, 'this': 0,
'with': 0, 'other': 0, 'has': 0, 'not': 0, "shouldve": 0, "shouldnt": 0,
'are': 0, 'don': 0, 'shan': 0, 'doing': 0, 'm': 0, 'they': 0, "youd": 0,
'having': 0, 'ours': 0, 'wasn': 0, 'did': 0, 'here': 0, "hadnt": 0, 're': 0,
'on': 0, 'very': 0, 'that': 0, 'above': 0, "werent": 0, "youve": 0,
'mustn': 0, 'will': 0, 'should': 0, 'couldn': 0, 'to': 0, 'there': 0, 'so': 0,
'itself': 0, 'our': 0, 'me': 0, "doesnt": 0, 'ma': 0, 'such': 0, 'further': 0,
'only': 0, 'the': 0, 'between': 0, 'y': 0, 'some': 0, 'him': 0, 'those': 0,
'won': 0, 'mightn': 0, 'nor': 0, 'being': 0, 'was': 0, 'themselves': 0,
'any': 0, "didnt": 0, 'my': 0, "wouldnt": 0, 'these': 0, 'she': 0, 'into': 0,
'am': 0, "youre": 0, 'where': 0, 'isn': 0, 'once': 0, 'it': 0, 'didn': 0,
'during': 0, 'about': 0, 'again': 0, 'aren': 0, 'yourselves': 0, 'theirs': 0,
'll': 0, "havent": 0, 'against': 0, 'then': 0, 'why': 0, 'o': 0, 'but': 0,
"dont": 0, 'shouldn': 0, 'up': 0, 'no': 0, 'because': 0, 'than': 0, 'does': 0,
'his': 0, 'when': 0, 'of': 0, 'whom': 0, 'from': 0, 'myself': 0}


# Stopword and stemming class
class StopWordStem:
    def __init__(self):
        pass

    # Method to remove stopwords and stemming
    def remove_and_stem(self, tokens):
        filtered_text = [stem(w) for w in tokens if w not in stop_words]
        more_filtered_text = [w for w in filtered_text if w not in stop_words]
        return more_filtered_text


# Tokenizer class
class Tokenizer:
    def __init__(self):
        pass

    # Method to tokenize
    def tokenize(self, text):
        text = text.lower()
        tokens = text.split()
        return tokens


# Index dictionary class
class Indexer:
    def __init__(self):
        pass

    # Method to create a counter dictionary
    def create_map(self, text):
        index = Counter(text)
        return index

    # Method to combine all the dictionaries by key values (words)
    def combine_maps(self, title, text, cat, info, links, refs):
        index = defaultdict(lambda: defaultdict(int))
        for k, v in chain(title.items(), text.items(), cat.items(), info.items(), links.items(), refs.items()):
            if k in title:
                if title[k] == v:
                    index[k]['t'] = v
            if k in text:
                if text[k] == v:
                    index[k]['b'] = v
            if k in cat:
                if cat[k] == v:
                    index[k]['c'] = v
            if k in info:
                if info[k] == v:
                    index[k]['i'] = v
            if k in links:
                if links[k] == v:
                    index[k]['l'] = v
            if k in refs:
                if refs[k] == v:
                    index[k]['r'] = v

        # return OrderedDict(sorted(index.items())
        return index
