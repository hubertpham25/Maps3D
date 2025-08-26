import xml.etree.ElementTree as ET

def tree_parser():
    tree = ET.parse('data/boston_map.osm')
    root = tree.getroot()

    nodes = dict() #nodes
    ways = dict() #edges
    addresses = dict()

    #starts at root node and finds everything that has 'node'
    for node in root.findall('node'):
        #grab node id, find coords, find node tags
        node_id = int(node.get('id'))
        lat = float(node.get('lat'))
        lon = float(node.get('lon'))

        coord = (lat, lon)

        street_num = ""
        street = ""
        store_name = ""
        # loop through all nodes and go through the tags
        for nd_tags in node.findall('tag'):
            k = nd_tags.get('k')
            v = nd_tags.get('v')

            if k == "addr:housenumber":
                if ("," in v) or ('-' in v):
                    continue
                street_num = v
            
            elif k == "addr:street":
                street = v

            elif k == "name":
                store_name = v
            
            # this loop should grab everything listed above and format it
            address = f"{street_num} {street.lower()}"
            if address and street:
                address = f"{street_num} {street.lower()}".strip()
                if address not in addresses:
                    addresses[address] = {
                        "info": [{
                            "store name": store_name,
                            "coord": coord,
                            "ID": node_id,
                        }]
                    }
                    
        nodes[node_id] = {
            'coord': coord,
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
            if (k == 'highway' and v == 'footway'):
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
    return nodes, ways, addresses

def get_street_names(addresses):
    street_names = list()
    for street_name in addresses:
        street_names.append(street_name)
    return sorted(street_names)

    
