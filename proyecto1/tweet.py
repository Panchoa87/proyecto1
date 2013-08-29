'''
Created on 04/08/2013

@author: Pancho
'''
import re
import conexion as conex
from nltk.corpus import stopwords
import normalizar as norma
import sys
class tweet():
    '''
    classdocs
    '''


    def __init__(self,tweetEvaluar,stpw):
        '''
        Constructor
        '''
        self.tweetOriginal=tweetEvaluar
        tweetLimpio=self.limpiar(tweetEvaluar)
        palabrasTweet=tweetLimpio.split()
        
        self.tweetwords=[]
        self.emoticonpos=0
        self.emoticonneg=0
        self.valence=0
        for i in range (len(palabrasTweet)):
            #print tweet[i]
            if palabrasTweet[i]=="emoticonpositivo":
                self.emoticonpos=self.emoticonpos+1
                #print ":)" 
            if palabrasTweet[i]=="emoticonegativo":
                self.emoticonneg=self.emoticonneg+1
                #print ":("
            
            if stpw=="0":
                if palabrasTweet[i] not in stopwords.words('spanish') and len(palabrasTweet[i]) > 1:
                    self.tweetwords.append(palabrasTweet[i])
                        
            if stpw=="1":
                self.tweetwords.append(palabrasTweet[i])
        
        for i in range (len(self.tweetwords)):
            if "@" in self.tweetwords[i]:
                self.tweetwords[i]="<MENCION>"
            if "#" in self.tweetwords[i]:
                self.tweetwords[i]="<HASHTAG>"
            if "www" in self.tweetwords[i] or "http" in self.tweetwords[i]:
                self.tweetwords[i]="<URL>"
            if "$" in self.tweetwords[i]:
                self.tweetwords[i]="<MONEDA>"
            if self.tweetwords[i].isdigit():
                self.tweetwords[i]="<NUMERO>"
                
        
        #self.__buscarPalabraDiccionario(self.tweetwords)
        self.__sacarPlural(self.tweetwords)
        self.tweetwords=norma.cambiarPalabras(self.tweetwords)
        
        
                
        
    def limpiar(self,tweetLimpiar):
        tweet=str(tweetLimpiar)        
        
        """ EMOTICONES 
        """
        tweet=tweet.replace(":)"," emoticonpositivo ")
        tweet=tweet.replace("XD"," emoticonpositivo ")
        tweet=tweet.replace("(:"," emoticonpositivo ")
        tweet=tweet.replace(":D"," emoticonpositivo ")
        tweet=tweet.replace(":-)"," emoticonpositivo ")
        tweet=tweet.replace("(-:"," emoticonpositivo ")
        tweet=tweet.replace("=D"," emoticonpositivo ")
        tweet=tweet.replace("=)"," emoticonpositivo ")
        tweet=tweet.replace("(="," emoticonpositivo ")
        tweet=tweet.replace(";-)"," emoticonpositivo ")
        tweet=tweet.replace(";)"," emoticonpositivo ")
        tweet=tweet.replace(";D"," emoticonpositivo ")
        tweet=tweet.replace("<3"," emoticonpositivo ")
        
        tweet=tweet.replace(":("," emoticonegativo ")
        tweet=tweet.replace("):"," emoticonegativo ")
        tweet=tweet.replace(":-("," emoticonegativo ")
        tweet=tweet.replace(")-:"," emoticonegativo ")
        tweet=tweet.replace("D:"," emoticonegativo ")
        tweet=tweet.replace("=D"," emoticonegativo ")
        tweet=tweet.replace("=("," emoticonegativo ")
        tweet=tweet.replace(")="," emoticonegativo ")
        tweet=tweet.replace(":'("," emoticonegativo ")
        tweet=tweet.replace("='["," emoticonegativo ")
        tweet=tweet.replace(":_("," emoticonegativo ")
        tweet=tweet.replace("/T_T"," emoticonegativo ")
        tweet=tweet.replace("TOT"," emoticonegativo ")
        tweet=tweet.replace(";_;"," emoticonegativo ")
        
        tweet=tweet.replace("RT"," ")
        
        tweet=tweet.lower()
        
        """ reg exp letras repetidas 
        """
        
        tweet=re.sub('a{2,}', 'a', tweet)
        tweet=re.sub('b{2,}', 'b', tweet)
        tweet=re.sub('c{2,}', 'c', tweet)
        tweet=re.sub('d{2,}', 'd', tweet)
        tweet=re.sub('e{2,}', 'e', tweet)
        tweet=re.sub('f{2,}', 'f', tweet)
        tweet=re.sub('g{2,}', 'g', tweet)
        tweet=re.sub('h{2,}', 'h', tweet)
        tweet=re.sub('i{2,}', 'i', tweet)
        tweet=re.sub('j{2,}', 'j', tweet)
        tweet=re.sub('k{2,}', 'k', tweet)
        tweet=re.sub('m{2,}', 'm', tweet)
        tweet=re.sub('n{2,}', 'n', tweet)
        tweet=re.sub('o{2,}', 'o', tweet)
        tweet=re.sub('p{2,}', 'p', tweet)
        tweet=re.sub('q{2,}', 'q', tweet)
        tweet=re.sub('s{2,}', 's', tweet)
        tweet=re.sub('u{2,}', 'u', tweet)
        tweet=re.sub('v{2,}', 'v', tweet)
        tweet=re.sub('w{2,}', 'w', tweet)
        tweet=re.sub('x{2,}', 'x', tweet)
        tweet=re.sub('y{2,}', 'y', tweet)
        tweet=re.sub('z{2,}', 'z', tweet)
        
        """ borro caracteres raros 
        """
        tweet=tweet.replace("/","")
        tweet=tweet.replace("*","")
        tweet=tweet.replace("\\","")
        tweet=tweet.replace("\"","")
        tweet=tweet.replace("%","")
        tweet=tweet.replace(";","")
        tweet=tweet.replace(",","")
        tweet=tweet.replace(":","")
        tweet=tweet.replace(".","")
        tweet=tweet.replace("?","")
        tweet=tweet.replace("!","")
        tweet=tweet.replace("\'","")
        tweet=tweet.replace("_","")
        tweet=tweet.replace("-","")
        tweet=tweet.replace("(","")
        tweet=tweet.replace(")","")
        tweet=tweet.replace("]","")
        tweet=tweet.replace("[","")
        tweet=tweet.replace("//","")
        tweet=tweet.replace("<","")
        tweet=tweet.replace(">","")
        
        return tweet    
    
        
    def __buscarPalabraDiccionario(self,tweetwords):
        ###  AQUI VEO SI LAS PALABRAS TIENEN VALOR EN ANEW ###        
        self.contval=1
        val=0
        anew=0
        for j in range (len(tweetwords)):
            #print tweetwords[j]
            conn=conex.conexion()
            conn.buscarPalabra(tweetwords[j])
            resultado=conn.getResultado()
            if len(resultado)>0:
                self.contval=self.contval+1
                for an in resultado:
                    anew=float(an[0])
                    val=anew+val
                    #print tweetwords[j]
        if self.contval==1:
            self.valence=0
            #print "sin valence"
        else:
            self.valence=float(val/(self.contval-1))    
            #print "valence "+str(valence)+ " por " +str(contval-1)+ " palabras"
    
        #if valence == 0:
        #    print "este tweet no cae dentro de anew"
        
        ###  FIN ANEW ###
    
    def __sacarPlural(self,tweetwords):
        leaves="s"
        for leaf in leaves:
            for i in range (len(tweetwords)):
                if tweetwords[i][-len(leaf):] == leaf:
                    self.tweetwords[i]=tweetwords[i][:-len(leaf)]
    
    def getEmoticonPos(self):
        return self.emoticonpos
    def getEmoticonNeg(self):
        return self.emoticonneg
    def getPalabrasTweet(self):
        return self.tweetwords
    def getTweet(self):
        return self.tweetOriginal
    def getValencia(self):
        return self.valence
    def getContVal(self):
        return self.contval