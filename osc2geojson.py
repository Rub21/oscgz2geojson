from sys import argv, exit
import xml.parsers.expat

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
        nodes.append(attrs['lat'] + ',' + attrs['lon'])
        refNodes[attrs['id']] = {
            'lat': attrs['lat'],
            'lon': attrs['lon']
        }

def end_element(name):
    global create
    create = (name == 'create')
    if name == 'osmChange':
        # write all nodes to file
        global nodes
        f.write('\n'.join(nodes))

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element

p.ParseFile(open(argv[1], 'r'))
