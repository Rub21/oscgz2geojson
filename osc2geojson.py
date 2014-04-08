from xml.etree.ElementTree import ElementTree
from sys import argv
from datetime import datetime
import time
import json
import gzip

f = gzip.open('484.osc.gz', 'rb')
file_content = f.read()

tree = ElementTree()

#tree.parse(file_content)

print file_content

f.close()