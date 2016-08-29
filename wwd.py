import os
import json
import sys
from os.path import basename
from xml.etree import cElementTree as ET

path = sys.argv[1]

for filename in os.listdir(path):
	if not filename.endswith('.xml'): continue

	fullname = os.path.join(path, filename)
	tree = ET.parse(fullname)
	root = tree.getroot()
	
	with open('input.txt', 'a') as inputtxt:
		# Start each line with the DocID and a tab.
		inputtxt.write(os.path.splitext(os.path.basename(filename))[0] + "\t")
		for fulltext in root.iter('FullText'):
			# Remove linebreaks and tabs, because every file is on its own line and tabs are used
			# to separate the docID's from the text itself.
			fulltext = fulltext.text.strip('\n\t')
			# Find words that have been hyphenated due to column width and re-connect them.
			fulltext = re.sub(r'([a-z])- ([a-z])', r'\1\2', fulltext)
			# Make sure the text is in the correct encoding.
			fulltext = fulltext.encode('utf-8')
			inputtxt.write(fulltext)
			# Start a new line.
			inputtxt.write("\n")
	
	jsoncatalogrecord = {}
	# This is an a awkward way to iterate over all elements in the XML tree. 
	# We need to find a way to create a loop over all elements, I think, 
	# rather than the specific ones listed below.
	for permalink in root.iter('URLDocView'):
		jsoncatalogrecord['searchstring'] =  '<a href="' + permalink.text + '">'
	for title in root.iter('RecordTitle'):
		jsoncatalogrecord['searchstring'] +=  title.text + '</a>'
	for title in root.iter('RecordTitle'):
		jsoncatalogrecord['title'] =  title.text 
	for author in root.iter('PersonName'):
		jsoncatalogrecord['author'] = author.text
	for date in root.iter('NumericPubDate'):
		jsoncatalogrecord['date'] = date.text[:4] + '-' +  date.text[4:6] + '-' + date.text[6:8]
	for genre in root.iter('objecttype'):
		jsoncatalogrecord['genre'] = genre.text
	
	print json.dumps(jsoncatalogrecord)
	with open('jsoncatalog.txt', 'a') as jsoncatalog:
		json.dump(jsoncatalogrecord, jsoncatalog)
		jsoncatalog.write('\n')
