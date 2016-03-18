import pyaudio
import sys
import time
import struct
import time
import wave
from numpy import mean, sqrt, square, power, fromstring, int16
import numpy as np

RMS_THRESHOLD = 500.0
RESULT_FILE_NAME = 'listen_mic_result.txt'


sound_detected = False


def writeResultFile(string):
    f = open(RESULT_FILE_NAME, 'a')
    f.write(string + '\n')
    f.close()

def callback(in_data, frame_count, time_info, status_flags):
        global sound_detected
        global rms_memory
        audio_data = fromstring(in_data, dtype=int16)
        audio_data = audio_data.astype(np.float32)
        audio_data = power(audio_data, 2)
        rms = sqrt(sum(audio_data/frame_count))
        print rms

        if ((rms > RMS_THRESHOLD) and (sound_detected == False)):
            writeResultFile(time.strftime("%Y-%m-%d %H:%M:%S") + '   -   sound detected')
            print(time.strftime("%Y-%m-%d %H:%M:%S") + '   -   sound detected')
            sound_detected = True
        elif ((rms < RMS_THRESHOLD) and (sound_detected == True)):
            writeResultFile(time.strftime("%Y-%m-%d %H:%M:%S") + '   -   sound not detected')
            print(time.strftime("%Y-%m-%d %H:%M:%S") + '   -   sound not detected')
            sound_detected = False
        else:
            None
        return (None, pyaudio.paContinue)


if __name__ == "__main__":
    CHUNK = 8192
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    stream_callback = callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    p.terminate()


