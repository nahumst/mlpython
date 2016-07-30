#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @ nahumst
# Cálculo de la entropía de una clase que tiene ejemplos positvos y negativos
# ver más : https://es.wikipedia.org/wiki/Entrop%C3%ADa_(información)

import math
import string
import numpy;

class Entropia: 
   # 'Clase '
    def __init__(self,valores): #valores[Clase, Positivos, Negativos]
        self.nombre=valores[0];
        self.valores=[];
        for i in range(1,len(valores)): #Transformamos Todo a Minusculas para la Facilitar la busqueda
            self.valores.append((string.lower(str(valores[i]))));
        #self.valores=valores[1:];
        self.positivos=-1;
        self.negativos=-1;
        self.total=len(valores)-1;
        self.entropia=0.0;
       
        
    def getPositivos(self): # Contamos los Positivos
        self.positivos=self.valores.count('si' or 'yes');
        return self.positivos;
    def getNegativos(self):# Contamos los Negativos
        self.negativos=self.valores.count('no' or 'not');
        return self.negativos;
        
    def getEntropia(self): # Calculamos la Entropia Total  

        if self.positivos < 0 :
            self.positivos=self.getPositivos();

        if self.negativos < 0 :
            self.negativos=self.getNegativos();
        
        print 'Calculo de Entropía Total\n','Clase:',self.nombre;
        print 'Total', self.total;
        print 'Positivos', self.positivos;
        print 'Negativos', self.negativos;   
        try:
            self.entropia= -(self.positivos/float(self.total)) * math.log(self.positivos/float(self.total),2) - (self.negativos/float(self.total))*math.log(self.negativos/float(self.total),2);
        except:
            self.entropia=0;
        return self.entropia;


testClase=Entropia(['JUGAR', 'No', 'No', 'Si', 'Si', 'Si', 'No', 'Si', 'No', 'Si', 'Si', 'Si', 'Si', 'Si', 'No']);
entropia=testClase.getEntropia();
print 'Entropia ',entropia;