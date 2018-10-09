import overpy
import geopy.distance
import subprocess

def make_csv(lat_org, lon_org, lat_dest, lon_dest):
  # 選択範囲の決定
  # 周囲約500mを選択 (緯度 15秒, 経度 22.5秒)
  lat_min = min([lat_org, lat_dest]) - 15 / 3600
  lat_max = max([lat_org, lat_dest]) + 15 / 3600

  lon_min = min([lon_org, lon_dest]) - 22.5 / 3600
  lon_max = max([lon_org, lon_dest]) + 22.5 / 3600

  # Overpass
  api = overpy.Overpass()

  qry = 'node(%f, %f, %f, %f); \
         way(bn)["highway"]; \
         (._; >;); \
         out;' % (lat_min, lon_min, lat_max, lon_max)

  result = api.query(qry)
  ways = result.ways

  with open('temporary/temp_nodes.csv', 'w') as node_file, open('temporary/temp_links.csv', 'w') as link_file:
    
    node_file.write('node_id,lat,lon,traffic_signal\n')
    link_file.write('node_id_org,node_id_dest,distance,highway,oneway\n')
    #link_file.write('node_id_org,node_id_dest,distance,highway,oneway,bridge,tunnel\n')

    for way in ways:
      highway = way.tags.get('highway') or ''
      oneway = way.tags.get('oneway') or ''
      #max_speed = way.tags.get('max_speed')
      #lanes = way.tags.get('lanes')
      #width = way.tags.get('width')

      #bridge = way.tags.get('bridge')
      #tunnel = way.tags.get('tunnel')

      #surface = way.tags.get('surface')
      #service = way.tags.get('service')
      #foot = way.tags.get('foot')
      #bicycle = way.tags.get('bicycle')

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

        link_file.write('%d,%d,%f,%s,%s\n' % (
          node1.id, node2.id, dist, highway, oneway))

def simplify_road_network():
  cmd = 'SimplifyRoadNetwork-exe.exe'
  subprocess.run(cmd)
  print("simplify_road_network")

def shortest_path(lat_org, lon_org, lat_dest, lon_dest):
  cmd = 'Geography-exe.exe %f %f %f %f' % (lat_org, lon_org, lat_dest, lon_dest)
  a = subprocess.getoutput(cmd).replace(' ', '').split(',')
  print(a)

if __name__ == '__main__':
  # 緯度・経度を入力
  lat_org, lon_org = map(float, input('出発地の緯度・経度').replace(' ', '').split(','))
  lat_dest, lon_dest = map(float, input('到着地の緯度・経度').replace(' ', '').split(','))

  make_csv(lat_org, lon_org, lat_dest, lon_dest)
  simplify_road_network()
  shortest_path(lat_org, lon_org, lat_dest, lon_dest)
  
'''
qryNode = 'node(50.745, 7.17, 50.75, 7.2);\
            way(bn)["highway"];\
            node(w);\
            out;'
'''
