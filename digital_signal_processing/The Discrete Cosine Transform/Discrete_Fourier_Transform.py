# -*- coding: utf-8 -*-
"""
@author: Lucas_Henrique e Welligtton_Cavedo
"""


def sinal_cossenoidal(A,f0,Ra,p0,T):
	"""
    Funcao que gera o sinal de acordo com os paramentros do problema,
    quai sejam:
        A: amplitude do sinal [V]
        f0: frequencia do sinal [Hz]
        p0: mudanca de fase [rad]
        Ra: taxa de sobre-amostragem (sobre a minima de Nyquist)
        T: numero de ciclos do sinal
    """
    
	fs = 2*Ra*f0                         #frequencia de amostragem**
	t = np.arange(0, T*1/f0-1/fs, 1/fs)  #suporte temporal
	g = A*np.cos(2*np.pi*f0*t+p0)        #sinal cossenoidal g(t)=2*pi*f*p
	return (t,g)                         #retorno funcional g(t)


"""
Ambiente de teste: sinal cossenoidal a uma dada taxa de amostragem
"""
import numpy as np
import matplotlib.pyplot as plt 

A = 2               #Amplitude max e min +1 e -1 V
f0 = 20             #frequencia = 20 Hz
#-------------
Ra = 20             #Taxa/Fator de sobreamostragem Ra = fs/2*f0, ou seja, 
                    # respeitar Nyquist estritamente significa deixar 
                    # este fator igual a unidade --> computacionalmente nao funciona
#-------------
fs = 2*Ra*f0        #frequencia de amostragem**
#p0 = 1/3*np.pi     #deslocamento de fase = pi/3 radianos
p0 = 0
T = 5               #numero de ciclos do sinal

(t,x) = sinal_cossenoidal(A,f0,Ra,p0,T) #chama a funcao sobre os parametros do problema


#imprime via pyplot da matplotlib 
plt.plot(t,x, '--b') 
plt.title('Sinal cossenoidal A = '+str(A)+'V, f0 = '+str(f0)+' Hz, fs = 2*Ra*f0 = '+str(fs)+' Hz') 
plt.xlabel('tempo (s)') 
plt.ylabel('Amplitude (V)') 
plt.show() 

"""
Algumas observacoes quanto ao fator Ra (Taxa de sobreamostragem)

Como o Python e uma linguagem interpretada, para obter um processamento
digital de uma senoide suave, a taxa de amostragem deve ser muito maior
que o minimo prescrito pela relacao de Nyquist-Shanon (pelo menos o dobro 
                                                       da max freq contida 
                                                       no sinal 2*f0)

Portanto precisamos amostrar o sinal de entrada a uma taxa significativamente
maior do que aquela que o criterio define - Aqui entra o fator de sobreamostragem
--> Computacionalmente quanto maior o fator de sobreamostragem, mais memoria
e necessaria para o armazenamento do sinal

"""


####-------------------------------

# Definindo uma discretizacao

# A propria funcao stem  do modulo pyplot da biblioteca matplotlib 
# Ref: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.stem.html

# ja oferece o sequenciamento dos valores da serie temporal como um conjunto
# discreto de argumentos, ou seja, plota um grafico de hastes com linhas verticais
# em cada localizacao x da linha de base para y, colocando um ponto de marcacao ali

####-------------------------------
#'''
largura_cm = 20
altura_cm = 20
pontos_por_cm = 150
plt.figure(
 figsize = (largura_cm, altura_cm),
 dpi = pontos_por_cm)
#'''
plt.stem(t,x, use_line_collection = True)
plt.title('Discretização do sinal anterior') 
plt.xlabel('n') 
plt.ylabel('g[n]') 
plt.plot(t,x)


 
####-------------------------------

# Obtendo a Transformada de Fourier

# Usaremos o algoritmo de Cooley-Tukey(1965) da FFT,
# uma implementacao otimizada da DFT de N-pontos 
# Uma excelente implementacao Python esta na biblioteca Scipy
# Ref: https://docs.scipy.org/doc/scipy/reference/fftpack.html


####---------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft

N = 1024            # numero de pontos amostrais (N pontos da DFT)    
G = fft(x,N)        # chama a funcao fft que recebe como paramentro o sinal e o numero de pontos 

#--- Imprimir os valores brutos de 0 a N --------

figura1, ax = plt.subplots(nrows=1, ncols=1) 
nVals = np.arange(start = 0,stop = N)         #de 0 a N sem shift de frequencia

ax.plot(nVals,np.abs(G))      
ax.set_title('Componentes frequenciais via FFT - sem deslocamento da componente DC')
ax.set_xlabel('Pontos de amostra da DFT')        
ax.set_ylabel('Valores da DFT')
figura1.show()

"""
Notar que a análise espectral do sinal nao esta correta
Deste grafico nao e possivel identificar a frequencia f0 do sinal cossenoidal
que geramos no item 1

Entao pergunta-se:
    
    Que relações devo obedecer para que o resultado da FFT seja adequado para
uma análise espectral correta de um sinal discreto?

Formalizaremos os seguintes procedimentos:
    - No dominio espectral as frequencias assumem valores positivos e negativos
    - Precisamos entao plotar os valors da DFT em um eixo de frequência com
    valores positivos e negativos e com o valor de indexacao 0 posicionado no meio
    
    a funcao fftshift da scipy realiza este shift de frequencia 
    da componente de frequência zero (DC) para o centro do espectro.
    
Vejamos:
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,fftshift


N = 1024    
X = fftshift(fft(x,N)) # chama a funcao fftfftshift que recebe como paramentro o sinal e o numero de pontos

figura2, ax = plt.subplots(nrows=1, ncols=1) 

#--- Imprimir os valores normalizados de -N/2  a  N/2  --------

fVals = np.arange(start = -N/2,stop = N/2)*fs/N  #de -N/2 a N/2 fatorizados pela taxa de amostragem

ax.plot(fVals,np.abs(X),'b')
ax.set_title('Componentes frequenciais via FFT - com deslocamento da componente DC')
ax.set_xlabel('Frequencia (Hz)')         
ax.set_ylabel('|Valores da DFT|')
ax.set_xlim((-f0-40),(f0+40))
ax.set_xticks(np.arange((-f0-40), (f0+40),10))
figura2.show()

"""
Agora e possivel visualizar que o valor absoluto de FFT
atinge o pico em +f0 e -f0 (No exemplo10 Hz e -10 Hz)

Os lóbulos laterais próximos aos valores de pico em 10 Hz e -10 Hz
são devidos ao vazamento espectral


"""









