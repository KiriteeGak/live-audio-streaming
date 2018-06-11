import pyaudio
import wave


class AudioRecorder(object):
    def __init__(self, audio_file_name):
        self.open = True
        self.rate = 44100
        self.frames_per_buffer = 1024
        self.channels = 2
        self.format = pyaudio.paInt16
        self.audio_filename = "{}.wav".format(audio_file_name)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []

    def record(self):
        self.stream.start_stream()
        while self.open:
            data = self.stream.read(self.frames_per_buffer)
            self.audio_frames.append(data)
            if not self.open:
                break

    def stop(self):
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            wave_file = wave.open(self.audio_filename, 'wb')
            wave_file.setnchannels(self.channels)
            wave_file.setsampwidth(self.audio.get_sample_size(self.format))
            wave_file.setframerate(self.rate)
            wave_file.writeframes(b''.join(self.audio_frames))
            wave_file.close()

    # Launches the audio recording function using a thread
    def start(self):
        self.record().start()
