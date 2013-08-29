'''
Created on 01/08/2013

@author: Pancho
'''
import MySQLdb

class conexion():
    '''
    classdocs
    '''


    def __init__(self,direccion="localhost",user="root",password="98312996",bd="analitic"):
        '''
        Constructor
        '''
        #abrir conexion bd
        self.db = MySQLdb.connect(direccion,user,password,bd)
        
        # prepare a cursor object using cursor() method
        self.c = self.db.cursor()
        
    def buscarPalabra(self,palabra):
        self.c.execute("SELECT valence FROM `anew` WHERE `word`='"+palabra+"'")
    
    def ejecutarSql(self,sql):
        self.c.execute(sql)
    
    def getResultado(self):
        return(self.c.fetchall())
    def cerrarConexion(self):
        self.db.close()
    def actualizar(self):
        self.db.commit()
    def prueba(self):
        c = self.db.cursor()
        c.execute("UPDATE `clasificar_proyecto` SET `netsense_w`='6' WHERE `id_articulo`='1000754324'")
        print self.db.commit()