read_audio = aifc.open(file[,rb])

channels, samplewidth, framerate, frames, comptype, compname = aifc.getparams()

write_audio = aifc.open(file[,wb])