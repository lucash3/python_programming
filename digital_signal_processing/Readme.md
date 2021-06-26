
## Digital Signal Processing in Python 📡

💻 Foundational DSP theory. Entire semester of “Signals and Systems”, a course within electrical engineering.

Here I utilize especially NumPy, which is Python’s standard library for arrays and high-level math. The codes also rely upon Matplotlib, which is a Python plotting library that provides an easy way to visualize signals, arrays, and complex numbers.
During the semester i've noted that while Python is “slower” than C++ in general, most math functions within Python/NumPy are implemented in C/C++ and heavily optimized. Likewise, the SDR API used is simply a set of Python bindings for C/C++ functions/classes. 

---

Throughout the course we've used generic complex baseband simulation techniques, to simulate several M-ary schemas, such as BPSK, FSK, AKS, PSK and QAM. 
We also simulate bit error rate performance (BER) over AWGN channel using complex baseband equivalent models.

<br>

The final project was the construction of a [full Modulator-Demodulator (MoDem) using object-oriented programming in Python](https://github.com/lucash3/python_programming/blob/main/digital_signal_processing/M-ary%20Digital%20Modulation%20Techniques/M-ary_Digital_Mod-Demod.ipynb)
