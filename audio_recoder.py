import pyaudio
import wave

from time import time


class AudioRecorder(object):
    """
    Rate is number of samples per second
    Chunk size is the amount of bytes a sample can contain
    E.g: To record five seconds of audio at a rate of say 16000Hz, we will be having 80000 sample.
    But each chunk can hold 1000 samples. So, if we have a loop with this,
     the appended array will have 80000/1000 = 80 samples.
    """

    def __init__(self, audio_file_name, recording_chunk_size=4):
        self.open = True
        self.frames_per_buffer = 256
        self.channels = 1
        self.format = pyaudio.paInt8
        self.audio_filename = "{}.wav".format(audio_file_name)
        self.folder_name = audio_file_name
        self.audio = pyaudio.PyAudio()
        self.rate = int(self.audio.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index=3,
                                      frames_per_buffer=self.frames_per_buffer)
        self.start_time = time()
        self.elapsed_time = None
        self.chunks = 0
        self.audio_frames = []
        self.recording_chunk_size = recording_chunk_size

    def record(self):
        self.stream.start_stream()
        chunk_start_time = time()
        while self.open:
            data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)
            self.audio_frames.append(data)

            if time()-chunk_start_time > self.recording_chunk_size:
                self.chunks += 1
                self._write_chunks()
                self.audio_frames = []
                chunk_start_time = time()

            if not self.open:
                break

    def stop(self):
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            self.elapsed_time = time()-self.start_time
            self._write_chunks()

    # Launches the audio recording function using a thread
    def start(self):
        self.record().start()

    def _write_chunks(self):
        import os
        if not os.path.exists("recordings/{}".format(self.folder_name)):
            os.makedirs("recordings/{}".format(self.folder_name))

        wavefile = wave.open("recordings/{}/chunk_{}.wav".format(self.folder_name, self.chunks), 'wb')
        wavefile.setnchannels(nchannels=self.channels)
        wavefile.setsampwidth(self.audio.get_sample_size(self.format))
        wavefile.setframerate(self.rate)
        wavefile.writeframes(b''.join(self.audio_frames))
        wavefile.close()

    def seek(self):
        pass
