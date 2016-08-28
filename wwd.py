import os
import json
import sys
from xml.etree import cElementTree as ET

path = sys.argv[1]

for filename in os.listdir(path):
	if not filename.endswith('.xml'): continue
	fullname = os.path.join(path, filename)

	tree = ET.parse(fullname)
	root = tree.getroot()
	
	jsoncatalogrecord = {}
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
