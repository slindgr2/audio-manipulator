import numpy as np
import aifc
import matplotlib.pyplot as plt

amplitude = np.array([1, 2, 3, 4])
frequency = np.fft.fft(amplitude)

amplitude = np.fft.ifft([frequency])[0]
print amplitude