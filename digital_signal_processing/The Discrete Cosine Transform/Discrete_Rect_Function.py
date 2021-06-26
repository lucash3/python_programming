# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 16:41:45 2020

@author: Lucas Henrique & Welligtton Cavedo

Implementacao de uma porta retangular de largura Tg e Taxa de amostragem Rg
Explorando o modulo  'Sinais e Sistemas' da biblioteca sigsys 
--> Ref: https://pypi.org/project/scikit-dsp-comm/

Caso a bilblioteca nao esteja disponivel no ambiente windows:

    ----------------------------------------------
    no CMD ou anaconda prompt:   pip install scikit-dsp-comm    
    ----------------------------------------------
"""


import matplotlib.pyplot as plt
import numpy as np
import sk_dsp_comm.sigsys as ss   #no CMD windows: pip install scikit-dsp-comm

##### Construção da porta retangular

Tg = 1      #Largura
Rg = 5      #Taxa de amostragem

t = np.arange(-5,5,1/Rg)
x0 = ss.rect(t-.5,Tg)

#figure, axis = plt.subplots(2, 1)

plt.figure(figsize=(6,5))
plt.plot(t,x0)

plt.ylim([-0.1,1.1])
plt.xlim([-2,2])
plt.title(r'Porta retangular de largura Tg = '+str(Tg))
plt.xlabel(r'Tempo (s)')
plt.ylabel(r'$g(t)$')
plt.show()


#### Versão discretizada (com um upscaling para melhor visualizacao)
#-->Descomentar trecho abaixo

largura_cm = 20
altura_cm = 20
pontos_por_cm = 150
plt.figure(
    figsize = (largura_cm, altura_cm),
    dpi = pontos_por_cm)
plt.stem(t,x0)
plt.title(r'Porta retangular de largura Tg = '+str(Tg))
plt.xlabel(r'Tempo (s)')
plt.ylabel(r'$g(t)$')
plt.show()




####### Implementacao da Transformada de Fourier (no Espectro) #####
Tg = 1
Rg = 100 

t = np.arange(-5,5,1/Rg)
x0 = ss.rect(t-.5,Tg)

f,X0 = ss.ft_approx(x0,t,4096)


plt.plot(f,abs(X0))
plt.xlim([-15,15])
plt.title(r'Espectro de magnitude')
plt.xlabel(r'Frequencia (Hz)')
plt.ylabel(r'$|G_0(f)|$');
plt.tight_layout()
plt.show()

##########################


##### Se quiser apresentar na mesma imagem ######
""" 
axis[0].set_title(r'Porta retangular de largura Tg = '+str(Tg))
axis[0].plot(t, x0)
axis[0].set_xlabel('tempo (s)')
axis[0].set_ylabel(r'$g(t)$')

axis[1].set_title(r'Espectro de magnitude')
axis[1].plot(f,abs(X0))
axis[1].set_xlabel(r'Frequencia (Hz)')
axis[1].set_ylabel(r'$|G_0(f)|$')

plotter.show()
"""


