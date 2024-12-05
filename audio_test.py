import pyaudio
import wave
import sys

chunk = 1024
p = pyaudio.PyAudio()
wf = wave.open(sys.argv[1], 'rb')

stream = p.open(format = p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(), rate = wf.getframerate(), output = True)

data = wf.readframes(chunk)
while data:
    stream.write(data)
    data = wf.readframes(chunk)

wf.close()
stream.close()
p.terminate()
