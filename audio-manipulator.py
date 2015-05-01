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
ave_freq = scipy.fftpack.rfft(ave_amp)

#This code filters out either the male or female voice depending on the user prompt. It also has the option to listen to both at the same time
frequencies = scipy.fftpack.fftfreq(len(ave_amp), 1.0 / rate) # Hertz
voice = raw_input('Which voice would you like to listen to? Male, Female, Both\n')
if voice == 'Male':
	# This loop was based on code written by Brady Garvin.
	for i in range(frames):
		if abs(frequencies[i]) > 1500:
			ave_freq[i] = 0
		else:
			ave_freq[i] = ave_freq[i] * 5
elif voice == 'Female':
	# This loop was based on code written by Brady Garvin.
	for i in range(frames):
		if abs(frequencies[i]) > 50 and abs(frequencies[i]) < 3000:
			ave_freq[i] = 0
		else: 
			ave_freq[i] = ave_freq[i] * 5
elif voice == 'Both':
	ave_freq = ave_freq
else:
	print 'Try again'

#This code converts our manipulated frequencies back into corresponding amplitudes.
output_amp = scipy.fftpack.irfft([ave_freq])[0]
output_amp = np.array(output_amp)

#This code writes our manipulated audio file so that it can be played though a media player.
write_audio = aifc.open("M1F1-mulawC-AFsp_output.aif","wb")
write_audio.setnchannels(1)
write_audio.setsampwidth(samplewidth)
write_audio.setframerate(rate)
write_audio.setcomptype(read_audio.getcomptype(), read_audio.getcomptype())
write_audio.writeframes(output_amp.astype(np.int16).tostring())
write_audio.close()