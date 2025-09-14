from lxml import etree

prefix = 'http://www.mediawiki.org/xml/export-0.10/'

context = etree.iterparse("./46gb/wiki-search.xml", events=('end',), tag='{'+prefix+'}page')

count = 0
f = open("./46gb/title_doc.txt", "w+")

for event, elem in context:
    count += 1

    idElem = elem.xpath('.//x:id', namespaces={'x': prefix})

    titleElem = elem.xpath('.//x:redirect', namespaces={'x': prefix})
    if not titleElem:
        titleElem = elem.xpath('.//x:title', namespaces={'x': prefix})
        f.write(idElem[0].text + " " + titleElem[0].text)
    else:
        f.write(idElem[0].text + " " + titleElem[0].get('title'))

    elem.clear()
    while elem.getprevious() is not None:
        del elem.getparent()[0]

print(count)
