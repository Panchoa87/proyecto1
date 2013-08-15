'''
Created on 02/08/2013

@author: Pancho
'''
import networkx as nx
class evaluacion():
    '''
    classdocs
    '''


    def __init__(self,tweetwords,red,emoticon,analisis,ponderadis,ponderapares):
        '''
        Constructor
        '''      
        self.distancia=0
        self.pares=1
        for k in range (len(tweetwords)-1):
            #print "Palabras " + str(tweetwords[k])+" y "+str(tweetwords[k+1]) +" en +"
            
            if tweetwords[k] in red.getNodos() and tweetwords[k+1] in red.getNodos():
                self.pares=self.pares+1
                
                #print str(tweetwords[k]) +" y "+str(tweetwords[k+1])  + " Estan presentes en G+"
                try:
                    if analisis==0:
                        dis=nx.shortest_path_length(red.getGrafo(),source=tweetwords[k],target=tweetwords[k+1])
                    if analisis==1:
                        dis=nx.shortest_path_length(red.getGrafo(),source=tweetwords[k],target=tweetwords[k+1],weight='weight')
                    #print "G Pos " + str(dis)
                    self.distancia=self.distancia+dis
                except nx.NetworkXNoPath, e:
                    dis=0
                    #print dis
                    #print "Entre "+ str(tweetwords[k])+" y "+str(tweetwords[k+1])+" no hay camino."
        
        
        self.promdis=float((self.distancia/self.pares)*float(ponderadis))
        self.costo=((self.promdis)/(self.getPares()**float(ponderapares))) - (emoticon)

    def getPares(self):
        return float(self.pares)
    def getDistancia(self):
        return float(self.distancia)
    def getPromedioDistancia(self):
        return float(self.promdis)
    def getCosto(self):
        return float(self.costo) 
    def setCosto(self,costo):
        self.costo=costo
    def debug(self,tipo="evaluacion"):
        print "-----------------------------------------------"
        print "Evaluacion: "+tipo
        print "Pares: "+str(self.pares)
        print "Distancia: "+str(self.distancia)
        print "Costo: "+str(self.costo)
        print "Promedio Distancia: "+str(self.promdis)
        print "-----------------------------------------------"    