from lxml import etree
import re

redirectPattern = re.compile("#"+"#REDIRECT"+"\s*\[\[(.*?)\]\]", re.I)
stubPattern = re.compile("\-"+"stub"+"\}\}", re.I)
disambiguationPattern = re.compile("\{\{"+"disambig"+"\}\}", re.I)
catPattern = re.compile("\[\[" + "Category" + ":(.*?)\]\]", re.I|re.M)

stylesPattern = re.compile("\{\|.*?\|\}$", re.S|re.M)
infoboxCleanUpPattern = re.compile("\{\{infobox(.*?)\}\}", re.S|re.M|re.I)
curlyCleanUpPattern0 = re.compile("^\{\{.*?\}\}$", re.S|re.M)
curlyCleanUpPattern1 = re.compile("\{\{.*?\}\}", re.S|re.M)
tagsPattern = re.compile("<.*>")
commentsCleanUpPattern = re.compile("<!--.*?-->", re.S|re.M)
linkPattern0 = re.compile("http.*[ ]")
linkPattern1 = re.compile("http.*[\n]")
cleanupPattern1 = re.compile("\[\[(.*?)\]\]", re.M|re.S)
numberPattern = re.compile("\d*[0-9][a-zA-Z\d]*")
quotePattern = re.compile("[']")
specCharsPattern = re.compile("[^A-Za-z0-9' ]")

class Parser():
	def __init__(self):
		pass

	def clean(self, text):
		text = re.sub(linkPattern0, " ", text)
		text = re.sub(linkPattern1, " ", text)
		text = re.sub(quotePattern, "", text)
		text = re.sub(stylesPattern, " ", text)
		text = re.sub(infoboxCleanUpPattern, " ", text)
		text = re.sub(catPattern, " ", text)
		text = re.sub(curlyCleanUpPattern0, " ", text)
		text = re.sub(curlyCleanUpPattern1, " ", text)
		text = re.sub(tagsPattern, " ", text)
		text = re.sub(commentsCleanUpPattern, " ", text)
		text = re.sub(specCharsPattern, " ", text)
		text = re.sub(numberPattern, " ", text)
		return text

	def parse_id(self, element):
		idElem = element.xpath('.//x:id',
						namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})
		return idElem[0].text

	def parse_title(self, element):
		titleElem = element.xpath('.//x:redirect',
						namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})
		if not titleElem:
			titleElem = element.xpath('.//x:title',
						namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})
			return self.clean(titleElem[0].text)
		else:
			return self.clean(titleElem[0].get('title'))

	def parse_cat(self, text):
		try:
			categories = re.findall(catPattern, text)
			categories = " ".join(categories)
			categories = self.clean(categories)
		except:
			categories = ""
		return categories

	def parse_infobox(self, text):
		try:
			infobox = re.findall(infoboxCleanUpPattern, text)
			infobox = " ".join(infobox)
			infobox = self.clean(infobox)
		except:
			infobox = ""
		return infobox

	def parse_link(self, text):
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
		return links

	def parse_text(self, element):
		textElem = element.xpath('.//x:text',
						namespaces={'x':'http://www.mediawiki.org/xml/export-0.8/'})

		categories = self.parse_cat(textElem[0].text)
		infobox = self.parse_infobox(textElem[0].text)
		links = self.parse_link(textElem[0].text)
		text = self.clean(textElem[0].text)

		return text, categories, infobox, links

	def parse_page(self, element):
		id = self.parse_id(element)
		title = self.parse_title(element)
		body, cat, info, links = self.parse_text(element)
		return id, title, body, cat, info, links