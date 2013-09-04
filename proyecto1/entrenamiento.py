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


    def __init__(self,tabla="",balan="0",stpw="0",ides=""):
        '''
        Constructor
        '''
        self.conn=conex.conexion()
        self.tabla=tabla
        if balan=="0":
            self.tabenlaces="enlaces_clasificador_0"
        if balan=="1":
            self.tabenlaces="enlaces_clasificador_1"
        sql="truncate "+self.tabenlaces
        self.conn.ejecutarSql(sql)
        self.conn.actualizar()
        balance=[]
        balance.append(self.__contarSentidoTweet(2,ides))#contar tweet negaticos
        balance.append(self.__contarSentidoTweet(1,ides))#contar tweet positivos
        balance.append(self.__contarSentidoTweet(0,ides))#contar tweet neutro
        balance=sorted(balance)
        
        if balan=="1":
            minimo=balance[0]
        if balan=="0":
            minimo=balance[2]
        
        self.__generarEntrenamiento(0, minimo,ides)
        self.__generarEntrenamiento(1, minimo,ides)
        self.__generarEntrenamiento(2, minimo,ides)
        
        self.conn.actualizar()
        self.conn.cerrarConexion()
        
    def __contarSentidoTweet(self,sentido,ides):
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`="+str(sentido)+" AND id_articulo NOT IN ("+ides+") "
        self.conn.ejecutarSql(sql)
        resultado=self.conn.getResultado()
        for valor in resultado:
            return(valor[0])
        
    def __generarEntrenamiento(self,sentido,min,ides):
        self.conn.ejecutarSql("SELECT cuerpo FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`="+str(sentido)+" AND id_articulo NOT IN ("+ides+") LIMIT "+str(min)+" ")
        resultado=self.conn.getResultado()
        cont=0
        aux=1
        for reg in resultado:
            #print aux
            aux=aux+1
            cuerpo=str(reg)
            cuerpo=norma.limpiar(cuerpo)
            cuerpo=cuerpo.split(' ')
            #print cuerpo
            #cuerpo arreglo de palabras
            #### TOKENIZACION
            palabras=norma.sacarSimbolos(cuerpo)
            palabras=norma.sacarPlural(palabras)
            palabras=norma.cambiarPalabras(palabras)
            palabras=norma.quitarVacios(palabras)

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
            
            #print "escribo enlaces en la base de datos"
            for ed in range (len(enlaces)):
                #enlaces=enlaces[ed]
                #print enlaces[ed].split(" ")
                links=enlaces[ed].split(" ")                       
                #print links[0],links[1],links[2]
                if links[0] not in stopwords.words('spanish') or links[1] not in stopwords.words('spanish') :
                    #print "INSERT INTO `"+str(tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`tabla`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','1','"+str(tabla)+"','0')"
                    sql="INSERT INTO `"+str(self.tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','"+str(sentido)+"','0')"
                    self.conn.ejecutarSql(sql)
                else:
                    sql="INSERT INTO `"+str(self.tabenlaces)+"`(`palabra_source`,`palabra_target`,`weight`,`sentido_manual`,`stop_word`) VALUES ('"+str(links[0])+"','"+str(links[1])+"','"+str(links[2])+"','"+str(sentido)+"','1')"
                    self.conn.ejecutarSql(sql)
            ### FIN BLOQUE PESOS ENLACES ###
            self.conn.actualizar()
        