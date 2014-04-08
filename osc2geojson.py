from sys import argv, exit
import xml.parsers.expat
import json

create = False
refNodes = {}
nodes = []
ways = []
f = open('nodes.datamap', 'w')

def start_element(name, attrs):
    global create
    global nodes
    global ways
    if name == 'create':
        create = True
    if create and name == 'node':
        nodes.append({
          "type": "Feature",
          "properties": {},
          "geometry": {
            "type": "Point",
            "coordinates": [attrs['lon'], attrs['lat']]
          }
        });
        refNodes[attrs['id']] = {
            'lat': attrs['lat'],
            'lon': attrs['lon']
        }

def end_element(name):
    global create
    create = (name == 'create')
    if name == 'osmChange':
        global nodes
        # write all nodes to file
        outNodes = '{"type": "FeatureCollection","features": ['

        for node in nodes:
            outNodes += json.dumps(node) + ','

        outNodes += ']}'
        f.write(outNodes)

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element

p.ParseFile(open(argv[1], 'r'))
