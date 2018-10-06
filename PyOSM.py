import overpy

def main():
  api = overpy.Overpass()

  qryWay = 'node(50.745, 7.17, 50.75, 7.2);\
            way(bn)["highway"];\
            (._; >;);\
            out;'
  
  qryNode = 'node(50.745, 7.17, 50.75, 7.2);\
             way(bn)["highway"];\
             node(w);\
             out;'
    
  result = api.query(qryWay)
  print(len(result.nodes))

if __name__ == '__main__':
  main()
