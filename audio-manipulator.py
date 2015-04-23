import numpy as np
import aifc

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
print amplitude

x = 0
while x < len(amplitude):
	if amplitude[x] > 128:
		amplitude[x] -= (amplitude[x] - (256**read_audio.getsampwidth()) /2 - 1)
	elif amplitude[x] < -128:
		amplitude[x] -= (amplitude[x] + 256**2/2 -1) #256**sampwidth /2 -1
	x += 1
	
print amplitude.real
print frequency
 
print read_audio.getframerate()