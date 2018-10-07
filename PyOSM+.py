import overpy
import geopy.distance

def main():

  api = overpy.Overpass()

  qry = 'node(50.745, 7.17, 50.75, 7.2);\
         way(bn)["highway"];\
         (._; >;);\
         out;'

  result = api.query(qry)
  ways = result.ways

  with open('temporary/temp_nodes.csv', 'w') as node_file, open('temporary/temp_links.csv', 'w') as link_file:
    node_file.write('node_id,lat,lon\n')
    link_file.write('node_id_org,node_id_dest,distance,highway,oneway,bridge,tunnel\n')

    for way in ways:
      highway = way.tags.get('highway')
      oneway = way.tags.get('oneway')
      bridge = way.tags.get('bridge')
      tunnel = way.tags.get('tunnel')

      nodes = way.nodes
      node_dict = {}

      for node in nodes:
        node_dict[node.id] = (node.lat, node.lon)
      
      for node_id, (lat, lon) in node_dict.items():
        node_file.write('%d,%f,%f\n' % (node_id, lat, lon))

      for node1, node2 in zip(nodes, nodes[1:]):
        coord1 = (node1.lat, node1.lon)
        coord2 = (node2.lat, node2.lon)
        dist = geopy.distance.vincenty(coord1, coord2).m

        link_file.write('%d,%d,%f,%s,%s,%s,%s\n' % (
          node1.id, node2.id, dist, highway, oneway, bridge, tunnel))


if __name__ == '__main__':
  main()
  
'''
      coords_1 = (52.2296756, 21.0122287)
      coords_2 = (52.406374, 16.9251681)
      geopy.distance.vincenty(coords_1, coords_2).m
    
      vert1 = vertIter.next()
      node1 = (vert1.x(), vert1.y(), layer)
      
      if node1 in nodes:
          nodeId1 = nodes[node1]
      else:
          nodes[node1] = nodeIdCount
          nodeId1 = nodeIdCount
          nodeIdCount += 1
          
          nodeFile.write('%d,%f,%f,%i\n' % (nodeId1, vert1.x(), vert1.y(), layer))
      
      while vertIter.hasNext():
          vert2 = vertIter.next()
          node2 = (vert2.x(), vert2.y(), layer)
          
          if node2 in nodes:
              nodeId2 = nodes[node2]
          else:
              nodes[node2] = nodeIdCount
              nodeId2 = nodeIdCount
              nodeIdCount += 1
              
              nodeFile.write('%d,%f,%f,%i\n' % (nodeId2, vert2.x(), vert2.y(), layer))
          
          #add links
          link = (nodeId1, nodeId2)
          
          if link not in links:
              pt1 = QgsPointXY(node1[0], node1[1])
              pt2 = QgsPointXY(node2[0], node2[1])
              
              dist = da.measureLine([pt1, pt2])
              
              if feat['fclass']:
                  fclass = feat['fclass']
              else:
                  fclass = ''
              
              if feat['oneway']:
                  oneway = feat['oneway']
              else:
                  oneway = ''
              
              if feat['bridge']:
                  bridge = feat['bridge']
              else:
                  bridge = ''
                  
              if feat['tunnel']:
                  tunnel = feat['tunnel']
              else:
                  tunnel = ''
              
              linkFile.write('%d,%d,%f,%s,%s,%s,%s\n' % (nodeId1, nodeId2, dist, fclass, oneway, bridge, tunnel))
              links.append(link)
          
          node1 = node2
          nodeId1 = nodeId2

qryNode = 'node(50.745, 7.17, 50.75, 7.2);\
            way(bn)["highway"];\
            node(w);\
            out;'
'''
