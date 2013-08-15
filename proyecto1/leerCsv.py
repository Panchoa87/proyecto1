'''
Created on 07/08/2013

@author: Pancho
'''
#!/usr/bin/env python
import csv
import normalizar as norm
import sys

if __name__ == '__main__':
    
    for i in range(1,4):
        reader = csv.reader(open('random'+str(i)+'.csv', 'rb'))
        archivo = csv.writer(open("random"+str(i)+"R.csv", "wb"))
        for index,row in enumerate(reader):
            if(row[3]=='0'):
                row[3]='"Neutro"'
            if(row[3]=='1'):
                row[3]='"Positivo"'
            if(row[3]=='2'):
                row[3]='Negativo'
            '''row[2]=norm.limpiar(row[2])
            palabras=row[2].split()
            palabras=norm.sacarSimbolos(palabras)
            palabras=norm.sacarPlural(palabras)
            palabras=norm.cambiarPalabras(palabras)
            palabras=" ".join(palabras)
            row[2]='"'+palabras+'"' '''
            row[2]='"'+str(row[2])+'"'
            archivo.writerow(row)
            print index