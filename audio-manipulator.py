import numpy as np
import aifc
import matplotlib.pyplot as plt
import scipy.fftpack

read_audio = aifc.open("M1F1-mulawC-AFsp.aif","rb")

# Stores audio info in variables
channels, samplewidth, rate, frames, comptype, compname = read_audio.getparams()

# Create a string of amplitudes for every frame.
amplitude = np.fromstring(read_audio.readframes(frames), np.int16)

# Amplitudes are derived from our frequency.
frequency = scipy.fftpack.rfft(amplitude)

amplitude = scipy.fftpack.irfft([frequency])[0].astype(np.int16)
print amplitude

#This code takes the amplitudes of our original file and clamps the amplitudes to the max amplitude that a speaker with the given sample width could hold.
amp_limit = (256**read_audio.getsampwidth()) / 2 - 1
x = 0
while x < len(amplitude):
	if amplitude[x] > amp_limit:
		amplitude[x] -= (amplitude[x] - amp_limit)
	elif amplitude[x] < - amp_limit:
		amplitude[x] -= (amplitude[x] + amp_limit) 
	x += 1
	
#averaging, The original file contains two voices in stereo format with n = 2 channels, this code takes the amplitudes of those channels and averages them into 1 mono channel. 
k = 0
z = 1
ave_amp = []
assert read_audio.getnchannels() == 2
while k < len(amplitude) -1 and z < len(amplitude):
	ave_amp.append((amplitude[k] + amplitude[z])/2)
	k += 2
	z += 2

ave_amp = np.array(ave_amp)	
print np.array(ave_amp)
ave_freq = scipy.fftpack.rfft(ave_amp)

plt.plot(list(range(len(ave_amp))), ave_amp, 'ro')
plt.show()
plt.plot(list(range(len(ave_freq))), ave_freq, 'ro')
plt.show()
plt.plot(list(range(len(frequency))), frequency, 'ro')
plt.show()

#print amplitude.real
#print frequency
#print read_audio.getnframes() 
#print read_audio.getframerate()

# Clamps our frequency to under 200 kHz
v = 0
while v < len(ave_freq):
	if ave_freq[v] > 200000:
		ave_freq[v] -= (ave_freq[v] + 200000)
	elif ave_freq[v] < -200000:
		ave_freq[v] -= (ave_freq[v] - 200000)
	v += 1

output_amp = scipy.fftpack.irfft([ave_freq])[0]
output_amp = np.array(output_amp)
#print output_amp
#plt.plot(list(range(len(output_amp))), output_amp, 'ro')
#plt.show()











# if true:
# 	play female voice
# elif true 
# 	play male voice
# elif true
# 	play original
# else
# 	print please choose an option.
# 	
	






write_audio = aifc.open("M1F1-mulawC-AFsp_output.aif","wb")
write_audio.setnchannels(1)
write_audio.setsampwidth(samplewidth)
write_audio.setframerate(rate)
write_audio.setcomptype(read_audio.getcomptype(), read_audio.getcomptype())
write_audio.writeframes(ave_amp.astype(np.int16).tostring())
write_audio.close()