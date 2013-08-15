'''
Created on 06/08/2013

@author: Pancho
'''
import conexion as conex
import normalizar as norma
from nltk.corpus import stopwords
import sys

class entrenamiento():
    '''
    classdocs
    '''


    def __init__(self,balan="0",tabla="",cantidad=1):
        '''
        Constructor
        '''
        self.conn=conex.conexion()
        self.tabla=tabla
        self.ides=""
        if balan=="0":
            self.tabenlaces="enlaces_clasificador_0"
        if balan=="1":
            self.tabenlaces="enlaces_clasificador_1"
            
        #Saco los tweets de prueba
        self.conn.ejecutarSql("SELECT id_articulo FROM `clasificar_"+str(self.tabla)+"` LIMIT 0,"+str(cantidad)+"")
        resultado=self.conn.getResultado()
        for registro in resultado:
            self.ides=str(self.ides)+str(registro[0])+","
        self.ides=str(self.ides[0:len(self.ides)-1])
        
        print self.ides
        
        balance=[]
        balance.append(self.__contarSentidoTweet(2,cantidad))#contar tweet negaticos
        balance.append(self.__contarSentidoTweet(1,cantidad))#contar tweet positivos
        balance.append(self.__contarSentidoTweet(0,cantidad))#contar tweet neutro
        balance=sorted(balance)
        print balance
        sys.exit(0)
        if balan=="1":
            minimo=balance[0]
        if balan=="0":
            minimo=balance[2]
        
        self.__generarEntrenamiento(0, minimo)
        self.__generarEntrenamiento(1, minimo)
        self.__generarEntrenamiento(2, minimo)
        
        #self.conn.actualizar()
        #self.conn.cerrarConexion()
        
    def __contarSentidoTweet(self,sentido,limit):
        self.conn.ejecutarSql("SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`="+str(sentido)+" AND id_articulo NOT IN ("+self.ides+")LIMIT "+str(limit)+" ")
        resultado=self.conn.getResultado()
        for valor in resultado:
            return(valor[0])
        
    def __generarEntrenamiento(self,sentido,min):
        self.conn.ejecutarSql("SELECT cuerpo FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`="+str(sentido)+" AND id_articulo NOT IN ("+self.ides+") LIMIT "+str(min)+" ")
        resultado=self.conn.getResultado()
        cont=0
        for reg in resultado:
            cuerpo=str(reg)
            cuerpo=norma.limpiar(cuerpo)
            
            #### TOKENIZACION
            palabras=[]
            for i in range (len(cuerpo)):
                #if cuerpo[i] not in stopwords.words('spanish') and len(cuerpo[i]) > 1:
                palabras.append(cuerpo[i])
                palabras=norma.sacarSimbolos(palabras)
                palabras=norma.sacarPlural(palabras)
                ### BLOQUE PESOS ENLACES ###
    
                pares=[]
                for i in range (len(palabras)+1):
                    if i<len(palabras)-1:
                #        print str(palabras[i]) +" -> "+ str(palabras[i+1]) + "\n"
                        pares.append(str(palabras[i])+" "+str(palabras[i+1]))
                
                enlaces=[]
                for w in pares:
                    #print w
                    
                    for w2 in pares:
                        if w == w2:
                            cont=cont+1
                            cont2=float(cont)
                    #print str(w)+" "+str(cont)
                    enlaces.append(str(w)+" "+str(1/cont2))
                    cont=0
                
                    print "escribo enlaces en la base de datos"
                    for ed in range (len(enlaces)):
                        #enlaces=enlaces[ed]
                        #print enlaces[ed].split(" ")
                        links=enlaces[ed].split(" ")
                        #print links[0],links[1],links[2]
                        if links[0] not in stopwords.words('spanish') or links[1] not in stopwords.words('spanish') :
                            #print "INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','1','"+str(tabla)+"','0')"
                            self.conn.ejecutarSql("INSERT INTO `"+str(self.tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','1','0')")
                        else:
                            self.conn.ejecutarSql("INSERT INTO `"+str(self.tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','1','1')")
                    ### FIN BLOQUE PESOS ENLACES ###
                