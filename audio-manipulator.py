import numpy as np
import aifc
import matplotlib.pyplot as plt

read_audio = aifc.open("M1F1-mulawC-AFsp.aif","rb")

channels, samplewidth, rate, frames, comptype, compname = read_audio.getparams()

write_audio = aifc.open("M1F1-mulawC-AFsp_output.aif","wb")
write_audio.setnchannels(channels)
write_audio.setsampwidth(samplewidth)
write_audio.setframerate(rate)
write_audio.setcomptype("NONE", "NONE")

amplitude = np.fromstring(read_audio.readframes(frames), np.int16)
frequency = np.fft.fft(amplitude)

amplitude = np.fft.ifft([frequency])[0]
amp_limit = (256**read_audio.getsampwidth()) / 2 - 1
x = 0
while x < len(amplitude):
	if amplitude[x] > amp_limit:
		amplitude[x] -= (amplitude[x] - amp_limit)
	elif amplitude[x] < - amp_limit:
		amplitude[x] -= (amplitude[x] + amp_limit) 
	x += 1

#averaging

k = 0
z = 1
v = 0
ave_amp = amplitude
while k < len(amplitude) -1 and z < len(amplitude):
	ave_amp[v] = (amplitude[k] + amplitude[z])/2
	k += 2
	z += 2
	v += 1 
	
plt.plot(list(range(len(ave_amp))), ave_amp, 'ro')
plt.show()
	










#plt.plot(list(range(len(frequency))), frequency, 'ro')
#plt.show()
#plt.plot(list(range(len(amplitude))), amplitude, 'ro')
#plt.show()
	
print amplitude.real
print frequency
print read_audio.getnframes() 
print read_audio.getframerate()