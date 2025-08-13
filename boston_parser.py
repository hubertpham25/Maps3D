import xml.etree.ElementTree as ET

def tree_parser():
    tree = ET.parse('boston_map.osm')
    root = tree.getroot()

    nodes = dict() #nodes
    ways = dict() #edges

    #starts at root node and finds everything that has 'node'
    for node in root.findall('node'):
        #grab node id, find coords, find node tags
        node_id = int(node.get('id'))
        lat = float(node.get('lat'))
        lon = float(node.get('lon'))
        nd_tags = {tag.get('k'): tag.get('v') for tag in node.findall('tag')}
        coord = (lat, lon)

        nodes[node_id] = {
            'coord': coord,
            'tags': nd_tags,
            'ways': set()
        }

    #starts at root node and finds everything that has 'node'
    for way in root.findall('way'):
        # loop should get the way id, 
        # node references (nodes that share ways), 
        # way tags. different from node tags
        way_id = int(way.get('id'))
        nd_ref = [int(nd.get('ref')) for nd in way.findall('nd')]
        #ignore footpaths
        way_tags = dict()
        for tag in way.findall('tag'):
            v = tag.get('v')
            k = tag.get('k')
            if k == 'highway' and v == 'footway':
                continue
            way_tags[k] = v

        ways[way_id] = {'nodes': nd_ref,
                        'tags': way_tags}
        
        # loop should go through reference nodes in nd_ref (list), 
        # check if ref is a key in nodes, 
        # if yes, add the way id to 'ways'. ref nodes are nodes that are related some way.
        for ref in nd_ref:
            if ref in nodes:
                nodes[ref]['ways'].add(way_id)
    
