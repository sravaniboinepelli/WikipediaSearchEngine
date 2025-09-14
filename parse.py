import re

# Pattern for redirects
redirectPattern = re.compile("#"+"#REDIRECT"+"\s*\[\[(.*?)\]\]", re.I)
# Pattern for stubs
stubPattern = re.compile("\-"+"stub"+"\}\}", re.I)
# Pattern for disambiguation
disambiguationPattern = re.compile("\{\{"+"disambig"+"\}\}", re.I)
# Pattern for categories
catPattern = re.compile("\[\[" + "Category" + ":(.*?)\]\]", re.I | re.M)
# Pattern for references
refPattern = re.compile("==References(?s)(?:(?!\n\n).)*")
# Pattern to remove references
removeRefPattern = re.compile("references", re.I)

# Pattern to clean up styles
stylesPattern = re.compile("\{\|.*?\|\}$", re.S|re.M)
# Pattern for infoboxes
infoboxCleanUpPattern = re.compile("\{\{infobox(.*?)\}\}", re.S | re.M | re.I)
# Patterns to remove strings in curly braces
curlyCleanUpPattern0 = re.compile("^\{\{.*?\}\}$", re.S | re.M)
curlyCleanUpPattern1 = re.compile("\{\{.*?\}\}", re.S | re.M)
# Pattern to remove inline tags
tagsPattern = re.compile("<.*>")
# Pattern to clean up comments
commentsCleanUpPattern = re.compile("<!--.*?-->", re.S | re.M)
# Pattern to remove links
linkPattern0 = re.compile("http.*[ ]")
linkPattern1 = re.compile("http.*[\n]")
# Pattern to clean up and for links
cleanupPattern1 = re.compile("\[\[(.*?)\]\]", re.M | re.S)
# Pattern to clean alphanumerics
numberPattern = re.compile("\d*[0-9][a-zA-Z\d]*")
# Pattern to clean apostrophes
quotePattern = re.compile("[']")
# Pattern to remove special characters
specCharsPattern = re.compile("[^A-Za-z0-9' ]")


# Parser class
class Parser:
    def __init__(self, prefix=None):
        self.prefix = prefix

    # Method to clean text
    def clean(self, text):
        text = re.sub(linkPattern0, " ", text)
        text = re.sub(linkPattern1, " ", text)
        text = re.sub(cleanupPattern1, " ", text)
        text = re.sub(quotePattern, "", text)
        text = re.sub(stylesPattern, " ", text)
        text = re.sub(infoboxCleanUpPattern, " ", text)
        text = re.sub(catPattern, " ", text)
        text = re.sub(refPattern, " ", text)
        text = re.sub(curlyCleanUpPattern0, " ", text)
        text = re.sub(curlyCleanUpPattern1, " ", text)
        text = re.sub(tagsPattern, " ", text)
        text = re.sub(commentsCleanUpPattern, " ", text)
        text = re.sub(specCharsPattern, " ", text)
        # text = re.sub(numberPattern, " ", text)
        return text

    # Method to parse id
    def parse_id(self, element):
        # Find the id element
        idElem = element.xpath('.//x:id', namespaces={'x': self.prefix})
        return idElem[0].text

    # Method to parse title
    def parse_title(self, element):
        # Find the title element
        titleElem = element.xpath('.//x:redirect', namespaces={'x': self.prefix})
        if not titleElem:
            titleElem = element.xpath('.//x:title', namespaces={'x': self.prefix})
            return self.clean(titleElem[0].text)
        else:
            return self.clean(titleElem[0].get('title'))

    # Method to parse categories
    def parse_cat(self, text):
        try:
            categories = re.findall(catPattern, text)
            categories = " ".join(categories)
            categories = self.clean(categories)
        except:
            categories = ""
        return categories

    # Method to parse infobox
    def parse_infobox(self, text):
        try:
            infobox = re.findall(infoboxCleanUpPattern, text)
            infobox = " ".join(infobox)
            infobox = self.clean(infobox)
        except:
            infobox = ""
        return infobox

    # Method to parse links
    def parse_link(self, text):
        try:
            links = re.findall(cleanupPattern1, text)
            valLinks = []
            for l in links:
                temp = l.split("|")
                if not temp:
                    continue
                link = temp[0]
                if ":" not in link:
                    valLinks.append(link)
            links = self.clean(" ".join(valLinks))
        except:
            links = ""
        return links

    # Method to parse references
    def parse_refs(self, text):
        try:
            ref_list = re.findall(refPattern, text)
            references = " ".join(ref_list)
            # Needs its own specific cleanup
            references = re.sub(tagsPattern, " ", references)
            references = re.sub(curlyCleanUpPattern0, " ", references)
            references = re.sub(curlyCleanUpPattern1, " ", references)
            references = re.sub(linkPattern0, " ", references)
            references = re.sub(linkPattern1, " ", references)
            references = re.sub(quotePattern, "", references)
            references = re.sub(specCharsPattern, " ", references)
            references = re.sub(numberPattern, " ", references)
            references = re.sub(removeRefPattern, " ", references)
        except:
            references = ""
        return references

    # Method to parse body
    def parse_text(self, element):
        # Find the text element
        textElem = element.xpath('.//x:text', namespaces={'x': self.prefix})

        if textElem[0].text is not None:
            categories = self.parse_cat(textElem[0].text)
            infobox = self.parse_infobox(textElem[0].text)
            links = self.parse_link(textElem[0].text)
            references = self.parse_refs(textElem[0].text)
            text = self.clean(textElem[0].text)
        else:
            categories = ""
            infobox = ""
            links = ""
            references = ""
            text = ""

        return text, categories, infobox, links, references

    # Method to parse a document
    def parse_page(self, element):
        id = self.parse_id(element)
        title = self.parse_title(element)
        body, cat, info, links, refs = self.parse_text(element)
        return id, title, body, cat, info, links, refs
