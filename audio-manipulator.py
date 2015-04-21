import numpy as np
import aifc

#read_audio = aifc.open("aiff-16.snd","rb")

#channels, samplewidth, framerate, frames, comptype, compname = read_audio.getparams()

#write_audio = aifc.open("aiff-16.snd","wb")
#write_audio.setnchannels(channels)
#write_audio.setsampwidth(samplewidth)
#write_audio.framerate(framerate)
#write_audio.setcomptype("NONE", "NONE")

amplitude = np.array([40, -300, 200, -700, 100, -5, 1, -4, 6, -8, 9, -10])
frequency = np.fft.fft(amplitude)

amplitude = np.fft.ifft([frequency])[0]
print amplitude

x = 0
while x < len(amplitude):
	if amplitude[x] > 128:
		amplitude[x] -= (amplitude[x] - 128)
	elif amplitude[x] < -128:
		amplitude[x] += (amplitude[x] +128)
	x += 1
	
print amplitude.real
	