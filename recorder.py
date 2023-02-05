import pyperclip
import os
import azure.cognitiveservices.speech as speechsdk
import pyaudio
import wave

class Recorder:
    dictate_hungarian = True
    clipboard_enabled = False
    output_path = ''
    in_progress = False
    speech_recognizer: speechsdk.SpeechRecognizer
    counter = 0
    filename_prefix = "audio_"
    current_filename = ''
    subscription = ''
    region = ''

    def __init__(self, subscription, region):
        self.audio = pyaudio.PyAudio()
        self.subscription = subscription
        self.region = region

    def start_recording(self):
        self.wf = wave.open(self.current_filename, 'wb')
        self.wf.setnchannels(1)
        self.wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        self.wf.setframerate(44100)
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=44100,
                                      input=True,
                                      frames_per_buffer=1024,
                                      stream_callback=self.callback)
        self.stream.start_stream()

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()

    def __del__(self):
        self.audio.terminate()

    def callback(self, in_data, frame_count, time_info, status):
        print(self.current_filename)
        self.wf.writeframes(in_data)
        return (in_data, pyaudio.paContinue)

    def interpret_footage(self):
        speech_config = speechsdk.SpeechConfig(subscription=self.subscription, region=self.region)
        speech_config.speech_recognition_language="hu-HU" if self.dictate_hungarian else "en-US"

        audio_input = speechsdk.AudioConfig(filename=self.current_filename)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

        result = speech_recognizer.recognize_once_async().get()

        return result.text

    def append_to_output(self, output):
        if self.output_path == '':
            return

        mode = "a" if os.path.exists(self.output_path) else "w"
        with open(self.current_filename, mode, encoding='utf-8') as file:
            file.write(output)

    def Stop(self):
        self.stop_recording()
        output = self.interpret_footage()
        os.remove(self.current_filename)
        self.append_to_output(output)
        self.counter += 1
        if self.clipboard_enabled:
            pyperclip.copy(output)


    def Start(self):
        self.current_filename = self.filename_prefix + ("hun_" if self.dictate_hungarian else "eng_") + str(self.counter) + ".wav"
        self.start_recording()
