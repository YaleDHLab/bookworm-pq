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
		inputtxt.write(os.path.splitext(os.path.basename(filename))[0] + "\t")
		for fulltext in root.iter('FullText'):
			inputtxt.write(fulltext.text.strip('\n\t').encode('utf-8'))
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
	for genre in root.iter('Genre'):
		jsoncatalogrecord['genre'] = genre.text
	
	print json.dumps(jsoncatalogrecord)
	with open('jsoncatalog.txt', 'a') as jsoncatalog:
		json.dump(jsoncatalogrecord, jsoncatalog)
		jsoncatalog.write('\n')
