import overpy
import geopy.distance
import subprocess
import csv
from time import sleep

def make_csv(lat_org, lon_org, lat_dest, lon_dest):
  # 選択範囲の決定
  # 周囲約250mを選択 (緯度 7.5秒, 経度 11.25秒)
  lat_min = min([lat_org, lat_dest]) - 7.5 / 3600
  lat_max = max([lat_org, lat_dest]) + 7.5 / 3600

  lon_min = min([lon_org, lon_dest]) - 11.25 / 3600
  lon_max = max([lon_org, lon_dest]) + 11.25 / 3600

  # Overpass
  api = overpy.Overpass()

  qry = 'way(%f, %f, %f, %f)-> .w; \
          ( \
           way.w["highway" ~ "trunk"]; \
           way.w["highway" ~ "primary"]; \
           way.w["highway" ~ "secondary"]; \
           way.w["highway" ~ "tertiary"]; \
           way.w["highway" ~ "unclassified"]; \
           way.w["highway" ~ "residential"]; \
           way.w["highway" ~ "service"]; \
           way.w["highway" ~ "footway"]; \
           way.w["highway" ~ "pedestrian"]; \
          ) -> ._; \
          (._; >;); \
          out;' % (lat_min, lon_min, lat_max, lon_max)

  # way.w["highway" ~ "motorway"]; \

  '''
    qry = 'node(%f, %f, %f, %f); \
          way(bn)["highway"]; \
          (._; >;); \
          out;' % (lat_min, lon_min, lat_max, lon_max)
  '''

  result = api.query(qry)
  ways = result.ways

  with open('temporary/temp_nodes.csv', 'w') as node_file, open('temporary/temp_links.csv', 'w') as link_file:
    
    node_file.write('node_id,lat,lon,signal\n')
    link_file.write('node_id_org,node_id_dest,distance,highway,oneway,max_speed,lanes,width,bridge,tunnel,surface,service,foot,bicycle\n')

    for way in ways:
      highway = way.tags.get('highway') or ''
      oneway = way.tags.get('oneway') or ''
      max_speed = way.tags.get('max_speed') or ''
      lanes = way.tags.get('lanes') or ''
      width = way.tags.get('width') or ''

      bridge = way.tags.get('bridge') or ''
      tunnel = way.tags.get('tunnel') or ''

      surface = way.tags.get('surface') or ''
      service = way.tags.get('service') or ''
      foot = way.tags.get('foot') or ''
      bicycle = way.tags.get('bicycle') or ''

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

        link_file.write('%d,%d,%f,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (
          node1.id, node2.id, dist, highway, oneway, max_speed, lanes, width, bridge, tunnel, surface, service, foot, bicycle))
  
  print('make_csv')

def simplify_road_network():
  cmd = 'SimplifyRoadNetwork-exe.exe'
  subprocess.run(cmd)
  print("simplify_road_network")

def shortest_path(lat_org, lon_org, lat_dest, lon_dest):
  cmd = 'Geography-exe.exe %f %f %f %f' % (lat_org, lon_org, lat_dest, lon_dest)
  dist = subprocess.getoutput(cmd).replace(' ', '').split(',')
  print('shortest_path')
  return dist

def main2():
  lat_org, lon_org = map(float, input('出発地の緯度・経度').replace(' ', '').split(','))
  lat_dest, lon_dest = map(float, input('到着地の緯度・経度').replace(' ', '').split(','))

  make_csv(lat_org, lon_org, lat_dest, lon_dest)
  simplify_road_network()
  dist = shortest_path(lat_org, lon_org, lat_dest, lon_dest)

  print(dist)

def main1():
  with open('ignore/input/rawdata_lat_lon.csv', 'r', encoding='UTF-8') as fi, open('ignore/output/rawdata_distance.csv', 'w', encoding='UTF-8') as fo:
    fo.write('sample_id,dist_link,dist_org,dist_dest\n')

    # make_csv(lat_org, lon_org, lat_dest, lon_dest)
    # simplify_road_network()
    # dist = shortest_path(lat_org, lon_org, lat_dest, lon_dest)

    # print(dist)
    
    reader = csv.reader(fi)
    header = next(reader)

    for row in reader:
      sample_id = row[0]
      lat_org, lon_org, lat_dest, lon_dest = map(float, row[1:])
      try:
        make_csv(lat_org, lon_org, lat_dest, lon_dest)
        simplify_road_network()
        dist = shortest_path(lat_org, lon_org, lat_dest, lon_dest)
        dist1 = []
        for d in dist:
          dist1.append(d.replace('"', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', ''))
        dist_link, dist_org, dist_dest = map(float, dist1) # map(float, dist.replace('"', '').replace('[', '').replace(']', '').replace('(', '').replace(')', '').replace(' ', '').split(','))
        fo.write('%s,%f,%f,%f\n' % (sample_id, dist_link, dist_org, dist_dest))
        sleep(10)
      except:
        pass
    
'''
qryNode = 'node(50.745, 7.17, 50.75, 7.2);\
            way(bn)["highway"];\
            node(w);\
            out;'
'''

if __name__ == '__main__':
  main1()
