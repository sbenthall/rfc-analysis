import urllib2
import urllib
import re
import os
from pprint import pprint as pp
import csv
from bs4 import BeautifulSoup
import json
from gather import *
from datetime import *

RFC_INDEX_FILENAME = 'rfc-index.xml'

with open(RFC_INDEX_FILENAME, 'r') as xmlfile:
  xml = xmlfile.read()

  soup = BeautifulSoup(xml)
  
  rows = soup('rfc-entry')

  entries = list()

  for row in rows:
    entry = dict()
    entry['rfc_number'] = unicode(row.find('doc-id').string).encode('utf-8')
    pp(entry['rfc_number'])
    entry['title'] = unicode(row.find('title').string).encode('utf-8')
    
    date_string = ' '.join(['01', unicode(row.select('date > month')[0].string).encode('utf-8'), unicode(row.select('date > year')[0].string).encode('utf-8')])
    date_published = datetime.strptime(date_string, '%d %B %Y')
    entry['date_published'] = date_published.strftime('%Y-%m-%d').encode('utf-8')
    entries.append(entry)

  pp(len(entries))

  # entries = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in entries)]

  with open('rfc.json', 'wb') as jsonfile:
    jsonfile.write(json.dumps(entries))