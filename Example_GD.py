# -*- coding: utf-8 -*-
'''
Ejemplo Descenso del Gradiente.
Regresión Lineal.
Expresión mx+b;
'''
import numpy as np
import matplotlib.pyplot as plt

N = 11 # No. Ejemplos
xs = np.linspace(0,10,N)
b  = 3 # intercepto
m  = 5 # pendiente
ruido = np.random.randint(0,5,N) 
y = m*xs + b #+ ruido # mx + b

# Queremos encontrar el valor de m y b
theta   = np.random.rand(2) #iniciamos con m y b = 0
#j_theta = sum(((xs*theta[0] + theta[1]) - y ) ** 2 ) / 2.0 * N # Costo
hist_cost = list()
N_iter = 8000
lr  = 1e-2
tol = 1e-10 #Condición de paro
for i in xrange(N_iter):
    h_theta  = theta[0]*xs + theta[1] 
    #print h_theta
    #print y
    theta[0] = theta[0] + lr * (sum((y - h_theta) * xs))/float(N)
    theta[1] = theta[1] + lr * (sum(y - h_theta))/float(N)
    cost     = sum((y - h_theta)**2)/float(N)
    hist_cost.append(cost)
    if cost <= tol:
        print 'Stop, iter: ',i
        break

y_pred = theta[0]*xs + theta[1]

plt.figure(1)
plt.plot(xs,y,'ro')
plt.plot(xs,y_pred)

rmse  = np.sqrt(sum((y - y_pred)**2)/float(N))
print theta
print rmse

plt.figure(2)
plt.plot(np.array(hist_cost))
plt.show()
