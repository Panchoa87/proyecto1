
'''
Created on 30/07/2013

@author: Pancho
'''
import networkx as nx
import conexion as conex
import sys

class red():
    '''
    classdocs
    '''
    def __init__(self,sentido,stw=0,balance="0",umbral=1,tabla="enlaces_clasificador_sentido"):
        '''
        Constructor
        '''
        conn=conex.conexion()
        self.grafo = nx.DiGraph()
        if balance=="0":
            self.tabenlaces="enlaces_clasificador_0"
        if balance=="1":
            self.tabenlaces="enlaces_clasificador_1"
        sql="SELECT `palabra_source`,`palabra_target` FROM `"+self.tabenlaces+"` WHERE `sentido_manual`="+str(sentido)+" "
        conn.ejecutarSql(sql)
        resultadoC1=conn.getResultado()
        for reg1 in resultadoC1:
            self.grafo.add_edge(reg1[0],reg1[1])
        conn.cerrarConexion()
    
    def setBalance(self,balance):
        self.balance=1-(float(self.getNumeroNodos()))/balance
        
    def getBalance(self):
        return self.balance   
    
    def getNumeroNodos(self):
        return len(self.grafo.nodes())
    
    def getNumeroEnlaces(self):
        return len(self.grafo.edges())
    def getNodos(self):
        return self.grafo.nodes()
    def getGrafo(self):
        return self.grafo
    def prueba(self,weight):
        dis=nx.shortest_path_length(self.grafo,source="<MENCION>")
        print dis