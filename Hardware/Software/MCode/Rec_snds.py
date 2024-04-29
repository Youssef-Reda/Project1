import subprocess
import time
from pydub import AudioSegment
from pydub.playback import play


class Rec_Mic(object):

    def __init__(self):
        self.command_snd = "arecord", "-D", "dmic_sv", "-c2", "-r", "48000", "-f", "S32_LE", "-t", "wav", "-V", "mono", "-v", "rec_test.wav"
        # "arecord -D dmic_sv -c2 -r 48000 -f S32_LE -t wav -V mono -v rec_test.wav""
        cmdcpy = 'cp ~/Desktop/MCode/.asoundrc ~/.asoundrc'
        subprocess.call(cmdcpy, shell=True)

    def Mic_strt(self):
        self.child = subprocess.Popen(
            self.command_snd, stdout=subprocess.PIPE)
        time.sleep(10)
        self.child.terminate()

    def Flt_snd(self):
        audio_file = "rec_test.wav"

        snd = AudioSegment.from_wav(audio_file)

        snd_mono = snd.set_channels(1)
        snd_mono2 = snd_mono

        snd_stereo = AudioSegment.from_mono_audiosegments(snd_mono, snd_mono2)
        # snd_stereo = snd_mono.set_channels(2)

        snd_l = snd_stereo.low_pass_filter(250)

        snd_l_h = snd_l.high_pass_filter(50)

        # Normaize and increae volume by 21 dB
        snd_db_ = snd_l_h.normalize()
        snd_15_db_ = snd_db_ + 21

        # save the output as mp3
        snd_15_db_.export("rec_test.mp3", "mp3")

    def Play_snd(self):
        sound = AudioSegment.from_mp3('rec_test.mp3')
        play(sound)
        # time.sleep(10.5)

        # import pyaudio
        # import wave
        # import sys
        # import numpy as np

        # CHUNK = 48000  # frames to keep in buffer between reads
        # samp_rate = 48000  # sample rate [Hz]
        # pyaudio_format = pyaudio.paInt16  # 16-bit device
        # buffer_format = np.int32  # 16-bit for buffer
        # chans = 1  # only read 1 channel
        # dev_index = 1  # index of sound device

        # wf = wave.open('rec_test.wav', 'rb')

        # # instantiate PyAudio (1)
        # audio = pyaudio.PyAudio()

        # # stream open (2)
        # stream_op = audio.open(format=pyaudio_format, rate=samp_rate,
        #                        channels=chans, output_device_index=dev_index, output=True)

        # # play stream (3)
        # while len(data) > 0:
        #     data = wf.readframes(CHUNK)
        #     stream_op.write(data)

        # # close stream and terminate audio
        # stream_op.stop_stream()
        # stream_op.close()

        # audio.terminate()
        # # read data
