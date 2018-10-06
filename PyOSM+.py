import overpy

def main():
  api = overpy.Overpass()

  qry = 'node(50.745, 7.17, 50.75, 7.2);\
         way(bn)["highway"];\
         (._; >;);\
         out;'

  result = api.query(qry)
  ways = result.ways

  nodeFile = open('%s%soutput_nodes.csv' % (path, region), 'w')
  nodeFile.write('nodeId,x,y,layer\n')

  linkFile = open('%s%soutput_links.csv' % (path, region), 'w')
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
