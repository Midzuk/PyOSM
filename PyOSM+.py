import overpy

def main():
  api = overpy.Overpass()

  qry = 'node(50.745, 7.17, 50.75, 7.2);\
         way(bn)["highway"];\
         (._; >;);\
         out;'

  result = api.query(qry)
  ways = result.ways

  nodeFile = open('temporary/temp_nodes.csv', 'w')
  nodeFile.write('nodeId,x,y,layer\n')

  linkFile = open('temporary/temp_links.csv', 'w')
  linkFile.write('nodeIdOrg,nodeIdDest,distance,highway,oneway,bridge,tunnel\n')

  for way in ways:
    pass

if __name__ == '__main__':
  main()

'''
qryNode = 'node(50.745, 7.17, 50.75, 7.2);\
            way(bn)["highway"];\
            node(w);\
            out;'
'''
