from sys import argv, exit
import xml.parsers.expat
import json

minlat = 40.68636570811299
minlon = -74.06227111816406
maxlat = 40.885486181691945
maxlon = -73.84117126464844

create = False
refNodes = {}
nodes = []
ways = []
f = open('nodes.geojson', 'w')

def start_element(name, attrs):
    global create
    global nodes
    global ways
    if name == 'create':
        create = True
    if create and name == 'node':
        if float(attrs['lat']) >= minlat and float(attrs['lat']) <= maxlat and float(attrs['lon']) >= minlon and float(attrs['lon']) <= maxlon:
            nodes.append({
              "type": "Feature",
              "properties": {},
              "geometry": {
                "type": "Point",
                "coordinates": [float(attrs['lon']), float(attrs['lat'])]
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

        outNodes = outNodes[:-1] + ']}'
        f.write(outNodes)

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element

p.ParseFile(open(argv[1], 'r'))
