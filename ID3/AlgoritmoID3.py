#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Algoritmo iD3
# Sánchez Texis Nahúm

import os
import string
import math

class ID3:
    """Clase: Algoritmo iD3 - Aprendizaje Computacional.""";
               
    def __init__(self):
        #print "Algoritmo ID3";
        self.dataSetOriginal=[];   # Leido del Archivo CVS
        self.dataSetTranspuesta=[] # Transpuesta de la Original
        self.atributos=[];         # Datos de los Atributos
        self.clase=[];             # Datos de la Clase
        self.ganancias={};         # Diccionario para almacenar de manera temporal las ganancias    
    
    def getBest(self, datos): # Obtenemos el Atributo con mejor Ganancia para la Clase
        maximo=0.0;
        maximoItem='';       
        datos=datos[:]; 
        self.ganancias={};#limpiamos el diccionario de ganancias
        entropiaClase=self.entropiaClase(datos[-1]);#Evitamos la clase
        print 'Entropia Clase: ',entropiaClase;
        for listaA in datos[:-1] :
            self.ganancias[listaA[0]]=self.gananciaA(listaA,datos[-1],entropiaClase);
        
        print 'Ganancias : ', self.ganancias.items();  
 
        for k,v in self.ganancias.iteritems():
            if v >= maximo:
                maximo=v;
                maximoItem=k;
        print '**Máximo', maximo, maximoItem;    
        return maximoItem;
        
    def gananciaA(self ,listaA, listaC, entropiaClase): #Calculamos la ganancia de algún Atributo
        listaACopia=listaA[:];
        nombre=listaACopia[0];
        listaACopia.remove(nombre);
        conjuntoEtiquetas=set(listaACopia);
        print 'Set:',conjuntoEtiquetas;
        gananciaTmp=0.0;
        totalClase=float(len(listaC)-1);
        for etiqueta in conjuntoEtiquetas:
            totalEtiqueta=listaACopia.count(etiqueta);
            gananciaTmp+=(totalEtiqueta/totalClase)*self.entropiaAtributo(listaACopia, listaC,etiqueta);
        ganancia=entropiaClase-gananciaTmp;
        return ganancia;
    def entropiaClase(self, lista): #Calculo de Entropia para una Clase
       # nombre=lista[0];
       # print 'Nombre de la Clase ',nombre;
       # print lista;
        positivos=lista.count('si' or 'yes');
        negativos=lista.count('no' or 'not');
        total=float(negativos+positivos);
        try:
            entropia= -(positivos/total) * math.log(positivos/total,2) - (negativos/total)*math.log(negativos/total,2);
        except:
            entropia=0.0;
        return entropia;
    def entropiaAtributo(self, listaA, listaC, etiqueta):#Calculo de Entropia para un Atributo
        listaACopia=listaA[:];
        listaCCopia=listaC[:];
        nombreA=listaACopia[0]; # El nombre por convención siempre vendrá en la posición 0
        nombreC=listaCCopia[0];
       # print nombreA, listaACopia;
       # print nombreC, listaCCopia;
        try:
           # listaA.remove(nombreA);
            listaCCopia.remove(nombreC);
        except: print 'Error: al quitar los nombres de las listas';
                
        totalOcurrencias=float(listaACopia.count(etiqueta));
      #  print 'totalO',totalOcurrencias;
        totalPositivos=0.0;
        totalNegativos=0.0;
        indices=[];
        for i, elemento in enumerate(listaACopia) : #Encontramos los indices de las ocurrencias de la "etiqueta" en la lista de Atributos para su Conteo
            if etiqueta == elemento :
                indices.append(i);
        
        for i in indices : # Deacuerdo a los indices encontrados, contamos los positivos y negativos, tomando la lista de la clase
            if listaCCopia[i] == 'si' or listaCCopia[i] == 'yes':
                totalPositivos+=1;
            elif listaCCopia[i] == 'no' or listaCCopia[i] == 'not':
                    totalNegativos+=1;          
       # print totalPositivos, totalNegativos; # Debug Quitar
        
        try:
            entropia= -(totalPositivos/totalOcurrencias) * math.log(totalPositivos/totalOcurrencias,2) - (totalNegativos/totalOcurrencias)*math.log(totalNegativos/totalOcurrencias,2);
        except:
            entropia=0.0;
        print 'Etiqueta:', etiqueta, 'Entropia', entropia; 
        return entropia;
        
    def makeDesicionTree(self,dataOriginal, dataTranspuesta, attributes, target, recursion): #Arbol de Desición
        recursion += 1

        dataOriginal = dataOriginal[:];
        dataTranspuesta= dataTranspuesta[:];
        vals = [record[attributes.index(target)] for record in dataOriginal]
        default = self.mayor(attributes, dataOriginal, target);#dataTranspuesta?
        
        if not dataOriginal or (len(attributes) - 1) <= 0:
            return default

        elif vals.count(vals[1]) == len(vals)-1:
            return vals[1]
        else:
            best = self.getBest(dataTranspuesta)

            tree = {best:{}}
            examplesTranspuesta=[];
            
            for val in self.getValues(dataTranspuesta, attributes, best): #para cada etiqueta del atributo
            # Create a subtree for the current value under the "best" field
                examples = self.getExamples(dataOriginal, attributes, best, val)
                for i in range(len(examples[0])):
                    examplesTranspuesta.append([row[i] for row in examples]);
                newAttr = attributes[:]
                newAttr.remove(best)                
                subtree = self.makeDesicionTree(examples, examplesTranspuesta, newAttr, target, recursion)
                tree[best][val] = subtree
        #print 'tree',tree;
        return tree;
        
    def readCsv(self, ruta, archivo): #Función para Leer el Archivo de Datos
        fileName=os.path.join(ruta,archivo);
        f=open(fileName);
        #self.dataSetOriginal=1#[x.split(',') for x in f.readlines()];
        
        for line in f:
            line = line.strip("\r\n")
            line = string.lower(line); #convertimos todo a minusculas para facilitar el análisis
            self.dataSetOriginal.append(line.split(','))
        
        self.atributos = self.dataSetOriginal[0]
        #print self.atributos;
        #self.dataSetOriginal(attributes)
        #print self.dataSetOriginal;
        
        for i in range(len(self.dataSetOriginal[0])):
            self.dataSetTranspuesta.append([row[i] for row in self.dataSetOriginal]);
        
        print 'Datos Leidos:'
        print '----------------------------------------------------------------';
        for elements in self.dataSetOriginal:#Eliminar esta Parte
            print elements;
        print '----------------------------------------------------------------'
        self.clase=self.dataSetTranspuesta[-1];
        
    def getValues(self, data, attributes, attr): #obtenemos los valores para un Atributo
        values=[];
        for e in data:
            if e[0]==attr:
                values=e;
                break;
        values=values[1:];#quitamos el nombre del atributo;
        valores=set(values);
        return list(valores);

    def getExamples(self, data, attributes, best, val): #Obtenemos un subconjunto de Ejemplos
        examples = [[]]
        atributos=attributes[:];
        atributos.remove(best);
        index = attributes.index(best)
        for entry in data:
            if (entry[index] == val):
                newEntry = []
                for i in range(0,len(entry)):
                    if(i != index):
                        newEntry.append(entry[i])
                examples.append(newEntry)
        examples.insert(0,atributos);
        examples.remove([])
        return examples
    
    def run(self, nombreArchivo):#Ejecutamos la Clase ID3
        arbolDeDesicion={};
        self.readCsv(os.path.dirname(__file__),nombreArchivo);
        arbolDeDesicion=self.makeDesicionTree(self.dataSetOriginal,self.dataSetTranspuesta, self.atributos, 'jugar', 0);
        print '\n';
        print '-------------------------------------------------------------------------------------------------------';
        print 'Arbol de Desición Para la Clase :', self.atributos[-1];
        print '\n',arbolDeDesicion;
        print '-------------------------------------------------------------------------------------------------------';
    
    def mayor(self, attributes, data, target):
        valFreq = {}
        index = attributes.index(target)
        print index;
        for tuple in data:
            print "tuple",tuple;
            if (valFreq.has_key(tuple[index])):
                valFreq[tuple[index]] += 1 
            else:
                valFreq[tuple[index]] = 1
        max = 0;
        mayor = "";
        print "valf",valFreq;
        for key in valFreq.keys():
            if valFreq[key]>max:
                max = valFreq[key]
                mayor = key
        print "mayor-A",attributes;
        print "mayor-T",target;
        print "mayor-D",data;
        print "mayor-M",mayor;
        return mayor;
        
#end Class ID3
testId3= ID3();
testId3.run('ID3.csv.xls');
