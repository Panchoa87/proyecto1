'''
Created on 04/08/2013

@author: Pancho
'''
import conexion as conex
import sys
class resultado():
    '''
    classdocs
    '''


    def __init__(self,tabla,w):
        '''
        Constructor
        '''
        self.tabla=tabla
        self.w=w
        self.conn=conex.conexion()
    
    def analizar(self,id,positivo,neutro,negativo):
        #############################################################
        #########################DECISION############################
        #############################################################
    
      
        #### DECISION POR PARES
        
        if positivo.getPares() == 1 and neutro.getPares() == 1 and negativo.getPares() > 1:
            #print "el tweet es Negativo"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")
        
        if negativo.getPares() == 1 and neutro.getPares() == 1 and positivo.getPares() > 1:
            #print "el tweet es Positivo"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
        
        if negativo.getPares() == 1 and positivo.getPares() == 1 and neutro.getPares() > 1:
            #print "el tweet es Neutro"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
        
        if positivo.getPares() == 1 and negativo.getPares() == 1 and neutro.getPares() == 1:
            #print "el tweet es no se puede clasificar"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='5' WHERE `id_articulo`='"+str(id)+"'")
        
        #### DECISION POR COSTO DE PRODUCCION
        if positivo.getPares() > 1 and negativo.getPares() > 1 and neutro.getPares() > 1:
        
            if positivo.getCosto() > negativo.getCosto() and neutro.getCosto() > negativo.getCosto():
                #print "El Tweet es negativo"
                self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")
            if positivo.getCosto() < negativo.getCosto() and positivo.getCosto() < neutro.getCosto():
                #print "El Tweet es positivo"
                self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
            
            if neutro.getCosto() < negativo.getCosto() and neutro.getCosto() < positivo.getCosto():
                #print "El Tweet es neutro"
                self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
                
        #### DECISION POR COSTOS SIMILARES    
            if positivo.getCosto() < neutro.getCosto() and negativo.getCosto() < neutro.getCosto():
                if positivo.getCosto() == negativo.getCosto():
                    #print "El Tweet es neutro"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
            
            if positivo.getCosto() < negativo.getCosto() and neutro.getCosto() < negativo.getCosto():
                if positivo.getCosto() == neutro.getCosto():
                    #print "El Tweet es neutro"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
            
            if negativo.getCosto() < positivo.getCosto() and neutro.getCosto() < positivo.getCosto():
                if negativo.getCosto() == neutro.getCosto():
                    #print "El Tweet es neutro"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
        
        
        if positivo.getCosto()==0:
            if negativo.getCosto()==neutro.getCosto():
                #print "El Tweet es neutro"
                self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 
            else:
                if negativo.getCosto()>neutro.getCosto():
                    #print "El Tweet es neutro"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")     
                else:
                    #print "El Tweet es negativo"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")     
        
        
        if negativo.getCosto()==0:
            if positivo.getCosto()==neutro.getCosto():
                #print "El Tweet es neutro"
                self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 
            else:
                if positivo.getCosto()>neutro.getCosto():
                    #print "El Tweet es neutro"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")     
                else:
                    #print "El Tweet es positivo"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
        
        if neutro.getCosto()==0:
            if positivo.getCosto()==negativo.getCosto():
                #print "El Tweet es neutro"
                self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'") 
            else:
                if positivo.getCosto()>negativo.getCosto():
                    #print "El Tweet es negativo"
                    self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")     
                else:
                    #print "El Tweet es positivo"
                    sql="UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='1' WHERE `id_articulo`='"+str(id)+"'"
                    self.conn.ejecutarSql(sql)
        
        
        if neutro.getCosto()==0 and negativo.getCosto()==0 and positivo.getCosto()>0:
            #print "el tweet es positivo"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='1' WHERE `id_articulo`='"+str(id)+"'")
        
        
        if neutro.getCosto()==0 and positivo.getCosto()==0 and negativo.getCosto()>0:
            #print "el tweet es negativo"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='2' WHERE `id_articulo`='"+str(id)+"'")
        
        if negativo.getCosto()==0 and positivo.getCosto()==0 and neutro.getCosto()>0:
            #print "el tweet es neutro"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='0' WHERE `id_articulo`='"+str(id)+"'")
        
        
        
        if neutro.getCosto()==0 and positivo.getCosto()==0 and negativo.getCosto()==0:
            #print "el tweet es no se puede clasificar"
            self.conn.ejecutarSql("UPDATE `clasificar_"+str(self.tabla)+"` SET `"+str(self.w)+"`='5' WHERE `id_articulo`='"+str(id)+"'")
            
        ##print "_____________________________________________"    
        self.conn.actualizar()
    
    def estadisticas(self,ides):
        ####CALCULOS FINALES####
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        for reg in consulta:
            #print "Tweets totales evaluados: "+str(reg[0])
            Total=reg[0]
            
        
        self.conn.ejecutarSql("SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `"+str(self.w)+"`= 5 AND id_articulo IN("+ides+")")
        consulta=self.conn.getResultado()
        for reg in consulta:
            sineva=reg[0]
        
        print "Tweets sin clasificar: "+str((float(sineva)/float(Total))*100)+"%" +", "+ str(sineva) + " de " + str(Total)
        
        TP_u=0
        FP_u=0
        FN_u=0
        
        #print "PERFORMANCE"    
        #neutros
        print "Neutros"
        #f.write("\n_*_*_*_*_*_*_*_*_*_*\n")
        #f.write("Neutros \n")
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`=0 and `"+str(self.w)+"`= 0 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "TPn: "+str(reg[0])
            TPn=float(reg[0])
            TP_u=TP_u+TPn
        
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`!= 0 and `"+str(self.w)+"`= 0 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "FPn: "+str(reg[0])
            FPn=float(reg[0])
            FP_u=FP_u+FPn
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`=0 and `"+str(self.w)+"`!=0 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"    
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "FNn: "+str(reg[0])
            FNn=float(reg[0])
            FN_u=FN_u+FNn
            
        #print "TNn: "+str(Total-(TPn+FPn+FNn))
        TNn=float(Total-(TPn+FPn+FNn))
        
        #print "_*_*_*_*_*_*_*_*_*_*"
        if (TPn+FPn+FNn+TNn) !=0:
            accun=float((TPn+TNn)/(TPn+FPn+FNn+TNn))
            #print "Accuracy: " + str(accun)
        else:
            #print "Accuracy: No definido (/0)"
            accun=0
        
        if (TPn+FPn) !=0:
            self.pren=float((TPn)/(TPn+FPn))    
            print "Precission: " + str(self.pren)
        else:
            #print "Precission: No definido (/0)"
            pren=0
        
        if (TPn+FNn) !=0:
            self.recn=float((TPn)/(TPn+FNn))
            print "Recall: " + str(self.recn)
        else:
            #print "Recall: No definido (/0)"
            recn=0
        #try:
        #    print "F-1: "+str( 2*pren*recn/(pren+recn) )
        #    f.write("F-1: "+str( 2*pren*recn/(pren+recn) ))
        #except:
        #    pass
        print "_*_*_*_*_*_*_*_*_*_*"
        #f.write("\n_*_*_*_*_*_*_*_*_*_*\n")
        
        #positivos
        print "Positivos"
        #f.write("Positivos\n")
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`=1 and `"+str(self.w)+"`= 1 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "TPp: "+str(reg[0])
            TPp=float(reg[0])
            TP_u=TP_u+TPp
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`!= 1 and `"+str(self.w)+"`= 1 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "FPp: "+str(reg[0])
            FPp=float(reg[0])
            FP_u=FP_u+FPp
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`=1 and `"+str(self.w)+"`!=1 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "FNp: "+str(reg[0])
            FNp=float(reg[0])
            FN_u=FN_u+FNp
            
        #print "TNp: "+str(Total-(TPp+FPp+FNp))
        TNp=float(Total-(TPp+FPp+FNp))
        
        
        #print "_*_*_*_*_*_*_*_*_*_*"
        if (TPp+FPp+FNp+TNp) !=0:
            accup=float((TPp+TNp)/(TPp+FPp+FNp+TNp))
            #print "Accuracy: " + str(accup)
        else:
            #print "Accuracy: No definido (/0)"
            accup=0
        
        if (TPp+FPp) !=0:    
            self.prep=float((TPp)/(TPp+FPp))
            print "Precission: " + str(self.prep)
        else:
            #print "Precission: No definido (/0)"
            self.prep=0
        
        if (TPp+FNp) !=0:
            self.recp=float((TPp)/(TPp+FNp))
            print "Recall: " + str(self.recp)
        else:
            #print "Recall: No definido (/0)"
            self.recp=0
        #try:
        #    print "F-1: "+str( 2*prep*recp/(prep+recp) )
        #    #f.write("F-1: "+str( 2*prep*recp/(prep+recp) ))
        #except:
        #    pass
        print "_*_*_*_*_*_*_*_*_*_*"
        #f.write("\n_*_*_*_*_*_*_*_*_*_*\n")
        #NEGATIVOS
        
        print "Negativos"
        #f.write("Negativos\n")
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`=2 and `"+str(self.w)+"`= 2 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "TPng: "+str(reg[0])
            TPng=float(reg[0])
            TP_u=TP_u+TPng
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`!= 2 and `"+str(self.w)+"`= 2 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "FPng: "+str(reg[0])
            FPng=float(reg[0])
            FP_u=FP_u+FPng
        sql="SELECT COUNT(*) FROM `clasificar_"+str(self.tabla)+"` WHERE `sentido_manual`=2 and `"+str(self.w)+"`!=2 AND `"+str(self.w)+"`!= 5 AND id_articulo IN("+ides+")"    
        self.conn.ejecutarSql(sql)
        consulta=self.conn.getResultado()
        
        for reg in consulta:
            #print "FNng: "+str(reg[0])
            FNng=float(reg[0])
            FN_u=FN_u+FNng
            
        #print "TNng: "+str(Total-(TPng+FPng+FNng))
        TNng=float(Total-(TPng+FPng+FNng))
        
        #print "_*_*_*_*_*_*_*_*_*_*"
        if (TPng+FPng+FNng+TNng) !=0:
            accung=float((TPng+TNng)/(TPng+FPng+FNng+TNng))
            #print "Accuracy: " + str(accung)
        else:
            #print "Accuracy: No definido (/0)"
            accung=0
        
        if (TPng+FPng) !=0:    
            self.preng=float((TPng)/(TPng+FPng))
            print "Precission: " + str(self.preng)
        else:
            #print "Precission: No definido (/0)"
            self.preng=0
        
        if (TPng+FNng) !=0:
            self.recng=float((TPng)/(TPng+FNng))
            print "Recall: " + str(self.recng)
        else:
            #print "Recall: No definido (/0)"
            self.recng=0
        #try:
        #    print "F-1: "+str( 2*preng*recng/(preng+recng) )
        #    #f.write("F-1: "+str( 2*preng*recng/(preng+recng) ))
        #except:
        #    pass
        #print "_*_*_*_*_*_*_*_*_*_*"
        
        print "_*_*_*_*_*_*"
        print "microaverage"
        print "_*_*_*_*_*_*"
        
        #print str(TP_u)+" kkakaka"
        #print str(FP_u)+" kkakaka"
        #print str(FN_u)+" kkakaka"

        print "Precision: " + str(float(TP_u/(TP_u+FP_u)))
        self.microPRE=float(TP_u/(TP_u+FP_u))
        print "Recall: " + str(float(TP_u/(TP_u+FN_u)))
        self.microREC=float(TP_u/(TP_u+FN_u))
        print "F-measure: " + str(self.getMicroF1())
        print "_*_*_*_*_*_*"
        print "MACROaverage"
        print "_*_*_*_*_*_*"
        
        print "Precision: " + str(float(self.pren+self.prep+self.preng)/3)
        self.MACROPRE=float((self.pren+self.prep+self.preng)/3)
        print "Recall: " + str(float(self.recn+self.recp+self.recng)/3)
        self.MACROREC=float((self.recn+self.recp+self.recng)/3)
        print "F-measure: " + str(self.getMacroF1())    
        
        self.conn.cerrarConexion()
        
    def getPrecisionNeutros(self):
        return self.pren
    def getRecallNeutros(self):
        return self.recn
    
    def getPrecisionNegativos(self):
        return self.preng
    def getRecallNegativos(self):
        return self.recng
    
    def getPrecisionPositivos(self):
        return self.prep
    def getRecallPositivos(self):
        return self.recp
    
    def getMicroPrecision(self):
        return self.microPRE
    def getMicroRec(self):
        return self.microREC
    def getMacroPrecision(self):
        return self.MACROPRE
    def getMacroRec(self):
        return self.MACROREC
    def getMacroF1(self):
        return (2*self.MACROPRE*self.MACROREC/(self.MACROPRE+self.MACROREC))
    def getMicroF1(self):
        return (2*self.microPRE*self.microREC/(self.microPRE+self.microREC))