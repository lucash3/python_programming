# -*- coding: utf-8 -*-
"""

COMDIG - TAREFA 1 - QUESTAO 4
Implementacao de um trem de impulso periódico discreto

@author: Lucas Henrique 140150838 e Welligtton Cavedo  130018660
"""

##### Primeira tentativa: construir um trem de impulso discreto

import numpy as np
import matplotlib.pyplot as plt

Ts = 2                          #periodo entre pulsos                
Fs = 1000                       #frequencia de amostragem para discretizar              
t = np.arange(-6, 6, 1/Fs)      #intervalo de tempo

trem = np.zeros_like(t)         #Referência:comunidade opensource SciPy https://numpy.org/doc/stable/reference/generated/numpy.zeros_like.html
trem[::int(Fs*Ts)] = Ts         #Impulsos a cada T*Fs amostras

plt.plot(t, trem)


### Construir uma função que gera um trem de impulsos e
### Calcula sua Transformada de Fourier #############

def trem(T):
    result = np.zeros(len(t))
    result[::int(Fs*T)] = 1
    return result

def Transformada(x):
    
    """
    Faremos uso da funcao fft da biblioteca numpy
    a fftshift troca o vetor de saída de fft para o meio da exibicao do espectro
    girando os resultados de forma que o termo DC esteja no centro 
    isto e, de -pi/2 a pi/2
      """
    
    return np.fft.fftshift(np.fft.fft(x)) * Fs/len(x)
 
    
Fs = 60
t = np.arange(0, 2, 1/Fs)       #janela de tempo especificado (0 a 2s a cada intervalo 1/Fs)
f = np.linspace(-Fs/2, Fs/2, len(t), endpoint=False) #meio caminho entre -fs/2 e fs/2


######## Exemplo 1 - Tremp de impulsos de perído Ts_1 ############

Ts_1 = 0.1                #periodo entre os pulsos
C_Ts_1 = trem(Ts_1)       #chamando a função trem de impulsos sobre a janela de tempo especificada


#----------------
"""
alterar tamanho e resolucao da figura
"""
largura_cm = 20
altura_cm = 20
pontos_por_cm = 150
plt.figure(
    figsize = (largura_cm, altura_cm),
    dpi = pontos_por_cm)

plt.subplot(221); 
#plt.plot(t, C_Ts_1)
plt.stem(t, C_Ts_1)    
plt.gca().title.set_text('Trem de impulso Ts = '+str(Ts_1)+' s')

#----------------

plt.subplot(222); 
plt.plot(f, abs(Transformada(C_Ts_1)*Ts_1))
plt.gca().title.set_text('Trem de impulso F = 1/Ts = '+str(1/Ts_1)+' Hz')

#----------------








######## Exemplo 2 - Tremp de impulsos de perído Ts_2 ############
Ts_2 = 0.05             #periodo entre os pulsos
C_Ts_2 = trem(Ts_2)     #chamando a função trem de impulsos sobre a janela de tempo especificada



"""
alterar tamanho e resolucao da figura
"""
largura_cm = 20
altura_cm = 20
pontos_por_cm = 150
plt.figure(
    figsize = (largura_cm, altura_cm),
    dpi = pontos_por_cm)
#----------------
plt.subplot(223); 
#plt.plot(t, C_Ts_2)
plt.stem(t, C_Ts_2)
plt.gca().title.set_text('Trem de impulso Ts = '+str(Ts_2)+' s')
#----------------

plt.subplot(224); plt.plot(f, abs(Transformada(C_Ts_2)*Ts_2))
plt.gca().title.set_text('Trem de impulso F = 1/Ts = '+str(1/Ts_2)+' Hz')



"""
O ensaio acima é muito interessante:


A multiplicação no domínio do tempo corresponde à uma convolução no
domínio da frequência. Multiplicar por um trem de impulso portanto,
corresponde a uma convolucao com a DFT (ou FFT nesse caso) de um trem de impulso.

Como se constatou acima, a Transformada do trem também é um trem de impulso e 
quanto MAIS PROXIMOS no dominio do tempo MAIS ESPACADOS eles se tornam
no dominio da frequencia 
Ou seja, em geral, mais impulsos no domínio do tempo correspondem a menos
impulsos no domínio da frequência.  

Resumindo:
    - Pode-se enxergar a amostragem como uma multiplicação por um trem de impulso
    
    - Multiplicar por um trem de impulso corresponde à convoluir
    com um trem de impulso no domínio da frequência
    
    - A convolução com um trem de impulso faz várias cópias do espectro do sinal

"""