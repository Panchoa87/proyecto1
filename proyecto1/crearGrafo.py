'''
Created on 01-09-2013

@author: pancho
'''
import networkx as nx
import json
from networkx.readwrite import json_graph
import matplotlib.pyplot as plt

if __name__ == '__main__':
    g=nx.Graph()
    palabra="hola como estas amigo mio?"
    palabra=palabra.split(' ')
    for i in range(len(palabra)-1):
        g.add_edge(palabra[i], palabra[i+1])
        dis=nx.shortest_path_length(g,source=palabra[i],target=palabra[i+1])
    print nx.shortest_path_length(g,source="hola",target="mio?")
    
    palabra="hola amigo"
    palabra=palabra.split(' ')
    for i in range(len(palabra)-1):
        g.add_edge(palabra[i], palabra[i+1])
        dis=nx.shortest_path_length(g,source=palabra[i],target=palabra[i+1])
    print nx.shortest_path_length(g,source="hola",target="mio?")
    print g.edges()
    d = json_graph.node_link_data(g) # node-link format to serialize
    print d
    json.dump(d, open('pruebas/grafo.json','w'))
    