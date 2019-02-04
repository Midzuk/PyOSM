import overpy
import geopy.distance
import subprocess
import csv
from time import sleep

def make_csv(lat_min, lon_min, lat_max, lon_max):

    # Overpass
    api = overpy.Overpass()

    qry = 'way(%f, %f, %f, %f)-> .w; \
            ( \
            way.w["highway" ~ "trunk"]; \
            way.w["highway" ~ "primary"]; \
            way.w["highway" ~ "secondary"]; \
            way.w["highway" ~ "tertiary"]; \
            way.w["highway" ~ "unclassified"]; \
            ) -> ._; \
            (._; >;); \
            out;' % (lat_min, lon_min, lat_max, lon_max)

    # way.w["highway" ~ "motorway"]; \
    # way.w["highway" ~ "residential"]; \
    # way.w["highway" ~ "service"]; \
    # way.w["highway" ~ "footway"]; \
    # way.w["highway" ~ "pedestrian"]; \

    '''
        qry = 'node(%f, %f, %f, %f); \
            way(bn)["highway"]; \
            (._; >;); \
            out;' % (lat_min, lon_min, lat_max, lon_max)
    '''

    result = api.query(qry)
    ways = result.ways

    with open('temporary/temp_nodes.csv', 'w') as node_file, open('temporary/temp_links.csv', 'w') as link_file:
        
        node_file.write('node_id,latitude,longitude,signal\n')
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
                dist = geopy.distance.distance(coord1, coord2).m

                link_file.write('%d,%d,%f,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (
                node1.id, node2.id, dist, highway, oneway, max_speed, lanes, width, bridge, tunnel, surface, service, foot, bicycle))
    
    print('make_csv')

def simplify_road_network():
    cmd = 'SimplifyRoadNetwork-exe.exe'
    subprocess.run(cmd)
    print("simplify_road_network")


def main():
    make_csv(36.11770833, 139.0578125, 36.27395833, 139.2484375)
    simplify_road_network()

if __name__ == '__main__':
    main()