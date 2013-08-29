'''
Created on 06/08/2013

@author: Pancho
'''
import re
import conexion as conex
import sys

def limpiar(tweetLimpiar):
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

def sacarPlural(tweetwords):
    #recibe un arreglo
    leaves="s"
    for leaf in leaves:
        for i in range (len(tweetwords)):
            if tweetwords[i][-len(leaf):] == leaf:
                tweetwords[i]=tweetwords[i][:-len(leaf)]
    return tweetwords

def sacarSimbolos(palabras):
    #recibe un arreglo
    for i in range (len(palabras)):
        if "@" in palabras[i]:
            palabras[i]="<MENCION>"
        if "#" in palabras[i]:
            palabras[i]="<HASHTAG>"
        if "www" in palabras[i] or "http" in palabras[i]:
            palabras[i]="<URL>"
        if "$" in palabras[i]:
            palabras[i]="<MONEDA>"
        if palabras[i].isdigit():
            palabras[i]="<NUMERO>"
    return palabras

def cambiarPalabras(palabras):
    conn= conex.conexion()
    for i in range (len(palabras)):
        sql="SELECT destino FROM diccionario WHERE palabra='"+str(palabras[i])+"' "
        conn.ejecutarSql(sql)
        resultado=conn.getResultado()
        if(len(resultado)>0):
            palabras[i]=resultado[0][0]
    return palabras
def quitarVacios(palabras):
    aux=[]
    for i in palabras:
        if i !='':
            aux.append(i)
    return aux