import numpy as np
import aifc
import matplotlib.pyplot as plt

read_audio = aifc.open("M1F1-mulawC-AFsp.aif","rb")

channels, samplewidth, rate, frames, comptype, compname = read_audio.getparams()


amplitude = np.fromstring(read_audio.readframes(frames), np.int16)
frequency = np.fft.fft(amplitude)

#amplitude = np.fft.ifft([frequency])[0]
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
ave_amp = []
assert read_audio.getnchannels() == 2
while k < len(amplitude) -1 and z < len(amplitude):
	ave_amp.append((amplitude[k] + amplitude[z])/2)
	k += 2
	z += 2
 
	
#plt.plot(list(range(len(ave_amp))), ave_amp, 'ro')
#plt.show()
#plt.plot(list(range(len(ave_freq))), ave_freq, 'ro')
#plt.show()
#plt.plot(list(range(len(frequency))), frequency, 'ro')
#plt.show()
#plt.plot(list(range(len(amplitude))), amplitude, 'ro')
#plt.show()

ave_freq = np.fft.fft(ave_amp)

#print amplitude.real
#print frequency
#print read_audio.getnframes() 
#print read_audio.getframerate()


v = 0
while v < len(ave_freq):
	if ave_freq[v] > 200000:
		ave_freq[v] -= (ave_freq[v] + 200000)
	elif ave_freq[v] < -200000:
		ave_freq[v] -= (ave_freq[v] - 200000)
	v += 1
#output_amp = np.fft.ifft([ave_freq])[0] / (amp_limit +1)


#plt.plot(list(range(len(ave_freq))), ave_freq, 'ro')
#plt.show()


write_audio = aifc.open("M1F1-mulawC-AFsp_output.aif","wb")
write_audio.setnchannels(1)
write_audio.setsampwidth(samplewidth)
write_audio.setframerate(rate)
write_audio.setcomptype(read_audio.getcomptype(), read_audio.getcomptype())
write_audio.writeframes(amplitude)
write_audio.close()