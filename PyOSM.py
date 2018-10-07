import overpy
import pyproj

def main():
  api = overpy.Overpass()

  qryWay = 'node(50.745, 7.17, 50.748, 7.18);\
            way(bn)["highway"];\
            (._; >;);\
            out;'
  
  qryNode = 'node(50.745, 7.17, 50.75, 7.2);\
             way(bn)["highway"];\
             node(w);\
             out;'
    
  result = api.query(qryWay)

  way = result.ways[0]

  #print(way.nodes)

  #print(result.nodes[0])

  nodes = way.get_nodes()
  node = nodes[0]

  print(node.data)

if __name__ == '__main__':
  main()
