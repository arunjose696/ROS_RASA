import rclpy
from rclpy.node import Node

from datetime import datetime
import requests
import time
import speech_recognition as sr
import threading
import multiprocessing
from custom_action_interfaces.action import Tts
print("dadad")

whisper_config={'no_speech_threshold':0.1, "condition_on_previous_text": False, "logprob_threshold": -1.00, "without_timestamps":True}
whisper_model_name = "base"
class Listener(Node):
    def __init__(self):
        super().__init__("listener") 
        #self.timer = self.create_timer(0.5, self.callback)
        
        print("starting to listen")
        self.get_logger().info('The listener now starts to listen')
        recognizer = sr.Recognizer()
        self.listen_and_recognize(recognizer)

    def listen_and_recognize(self,recognizer):
        with sr.Microphone(device_index=0) as source:
            while True:
                print("Say something!")
                audio = recognizer.listen(source)
                print("start transcription")
                try:
                    text = recognizer.recognize_google(audio)
                    print("Google Speech Recognition:", text)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition:", e)
                try:
                    whisper_transcription = recognizer.recognize_whisper(audio, model=whisper_model_name, language="english",**whisper_config)
                    print("Whisper thinks you said " + whisper_transcription)
                    if whisper_transcription:
                        
                        url = ' http://localhost:5005/webhooks/myio/webhook'
                        myobj = { "sender": "test_user", "message": whisper_transcription, "metadata": {}, "text":whisper_transcription }
                        x = requests.post(url, json = myobj)
                        print(x.content)
                except sr.UnknownValueError:
                    print("Whisper could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Whisper")
    
    # def process_audio(self,recognizer):
    #     while True:
    #         if True:    
    #             try:
    #                 text = recognizer.recognize_google(audio)
    #                 print("Google Speech Recognition:", text)
    #             except sr.UnknownValueError:
    #                 print("Could not understand audio")
    #             except sr.RequestError as e:
    #                 print("Could not request results from Google Speech Recognition:", e)
                
    #             try:
    #                 whisper_transcription = recognizer.recognize_whisper(audio, language="english")
    #                 url = ' http://localhost:5005/webhooks/myio/webhook'
                    
    #                 print("Whisper thinks you said " + whisper_transcription)
    #                 if whisper_transcription:
    #                     x = requests.post(url, json = myobj)

    #             except sr.UnknownValueError:
    #                 print("Whisper could not understand audio")
    #             except sr.RequestError as e:
    #                 print("Could not request results from Whisper")
    
    

    
def main(args=None):
    rclpy.init(args=args)
    node = Listener() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
