import wave
import pyaudio


def record_to_file(format_=pyaudio.paInt16,
                   channels_=1,
                   rate_=8000,
                   chunk_=1024,
                   seconds_=10,
                   chunk_seconds_save=4,
                   podcast_name="sample_podcast"):

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format_,
                        channels=channels_,
                        rate=rate_,
                        input=True,
                        frames_per_buffer=chunk_)
    frames = []

    for i in range(0, int(rate_ / rate_ * seconds_)):
        data = stream.read(rate_)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    write_by_chunks(chunk_seconds_save, frames, channels_, format_, audio, rate_, podcast_name)


def write_by_chunks(chunk_seconds_save, chunk_list, channels_, format_, audio, rate_, podcast_name):

    import os

    if not os.path.exists("recordings/{}".format(podcast_name)):
        os.makedirs("recordings/{}".format(podcast_name))
    for index_ in range(chunk_seconds_save, len(chunk_list)+chunk_seconds_save, chunk_seconds_save):
        print(index_)
        wavefile = wave.open("recordings/{}/{}".format(podcast_name, index_), 'wb')
        wavefile.setnchannels(channels_)
        wavefile.setsampwidth(audio.get_sample_size(format_))
        wavefile.setframerate(rate_)
        sub_list = chunk_list[index_-chunk_seconds_save:index_]
        wavefile.writeframes(b''.join(sub_list))
        wavefile.close()


record_to_file()
