import overpy
import geopy.distance

def main():

  api = overpy.Overpass()

  qry = 'node(35.635, 139.918, 35.647, 139.930);\
         way(bn)["highway"];\
         (._; >;);\
         out;'

  result = api.query(qry)
  ways = result.ways

  with open('temporary/temp_nodes.csv', 'w') as node_file, open('temporary/temp_links.csv', 'w') as link_file:
    
    node_file.write('node_id,lat,lon,traffic_signal\n')
    link_file.write('node_id_org,node_id_dest,distance,highway,oneway,bridge,tunnel\n')

    for way in ways:
      highway = way.tags.get('highway')
      oneway = way.tags.get('oneway')
      bridge = way.tags.get('bridge')
      tunnel = way.tags.get('tunnel')

      nodes = way.nodes
      node_dict = {}

      for node in nodes:
        node_highway = node.tags.get('highway')

        if node_highway == 'traffic_signals':
          node_dict[node.id] = (node.lat, node.lon, 'yes')
        else:
          node_dict[node.id] = (node.lat, node.lon, 'no')
      
      for node_id, (lat, lon, signal) in node_dict.items():
        node_file.write('%d,%f,%f,%s\n' % (node_id, lat, lon, signal))

      for node1, node2 in zip(nodes, nodes[1:]):
        coord1 = (node1.lat, node1.lon)
        coord2 = (node2.lat, node2.lon)
        dist = geopy.distance.vincenty(coord1, coord2).m

        link_file.write('%d,%d,%f,%s,%s,%s,%s\n' % (
          node1.id, node2.id, dist, highway, oneway, bridge, tunnel))


if __name__ == '__main__':
  main()
  
'''
qryNode = 'node(50.745, 7.17, 50.75, 7.2);\
            way(bn)["highway"];\
            node(w);\
            out;'
'''
