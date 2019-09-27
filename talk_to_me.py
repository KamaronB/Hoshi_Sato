import pyttsx3
import speech_recognition as sp
import pyaudio
import time
import numpy
import wave
from trans_mover import TransMover
from playsound import playsound
import pandas as pd
import uuid
import os
import webbrowser
from hoshi_memory import Memory

class Hoshi:
    """Hoshi Satos voice by Kamaron Bickham. This class listens to a voice and creates a corresponding file. It
    then parses that file for words and translates them before speaking them back to you"""

    def __init__(self,file_name,currentDir,name='New user'):
    ##create a trans_mover
        trans=TransMover(currentDir)
        self.dir='/home/morty/hoshi/'
        self.file_name=self.dir+file_name
        self.listen=True
        self.trans=trans
        self.name= name

        self.threshold = 0.3 # volume threshold to trigger at, 0 is nothing 1 is max volume
        self.min_delay = 1 # min seconds between attempts
        self.last_run = 0 # helper for min_delay
        self.memory= Memory()

    # record sound
    def create_audio(self,seconds=5,Listening=False,other_file=''):

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = seconds
        WAVE_OUTPUT_FILENAME=''
        ##creates file for listening for her name and another for
        if Listening==False:
            WAVE_OUTPUT_FILENAME = self.file_name
        else:
            WAVE_OUTPUT_FILENAME = other_file

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)


        # self.speak('I am now listening')

        playsound('/home/morty/hoshi/beep2.wav')



        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        playsound('/home/morty/hoshi/beep2.wav')
        # self.speak(" done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()




    #function to recognize words
    def recognize(self,file2=''):
        #initialize a new recognizer & open audio file
        dir='/home/morty/hoshi/'
        rec = sp.Recognizer()
        if file2=='':
            voice_file= sp.AudioFile(self.file_name)
        else:
            voice_file=sp.AudioFile(dir+file2)
        print(type(voice_file))

        with voice_file as source:
            #record output to a file
            output= rec.record(source)

            #recognize the output from read source
        try:
            value = rec.recognize_google(output)
            answer= input(self.speak('would you like to hear this in another language. Please enter y or n'))
            if answer.lower()=='y':
                try:
                    print(value)
                    words =self.trans.translate(value)

                    self.speak(self.name + 'in spanish')
                    return(words)
                    # print(sentance)
                except:
                    self.speak(self.name +' My Translation service is not currently working. But without the')
                    return(value)
            else:
                self.speak(self.name)
                return(value)
        except:
            self.speak("Couldn't quite understand you")






    #speaking the words with pyttsx
    def speak(self,words):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Prints out different voices
        # for voice in voices:
        #     print(voice.gender)
        #     print(voice.id)
        engine.setProperty('voice', 'english+f1')
        engine.setProperty('rate',150)
        engine.say(words)
        engine.runAndWait()



    def listening(self,signal='go'):

      audio_sample_rate = 48e3
      audio_frame_samples = 1024*7

      left_channel = 1
      right_channel = 1
      try:
          _ = self.stream
      except AttributeError:
          pa = pyaudio.PyAudio()
          stream = pa.open(format=pyaudio.paInt16, channels=2,
                     rate=int(audio_sample_rate),
                     input=True,
                     frames_per_buffer=audio_frame_samples)
          self.stream = stream


      # turn the string into an array.
      raw_data = self.stream.read(audio_frame_samples) #read whole buffer.
      samples  = numpy.fromstring(raw_data, dtype=numpy.int16)
      # Normalize by int16 max (32767)
      normed_samples = samples / float(numpy.iinfo(numpy.int16).max)
      # split out the left and right channels to return separately.
      left_samples = normed_samples[left_channel::2]
      right_samples = normed_samples[right_channel::2]

      if signal=='stop':
          stream.close()
      return left_samples, right_samples


    def get_response(self):
          rec = sp.Recognizer()
          #create a random file name
          random_file= '/home/morty/hoshi/' + str(uuid.uuid4())+'.wav'

          #create the audio for listening
          self.create_audio(seconds=5,Listening=True,other_file=random_file)

          voice_file=sp.AudioFile(random_file)
          print(type(voice_file))

          with voice_file as source:
              #record output to a file
              output= rec.record(source)

              #recognize the output from read source
          try:
              value = rec.recognize_google(output)

              return(value)
          except:
              self.speak("Couldn't quite understand you")

    #for running commands
    def run_command(self,command):


         #Split command into list of words
         command=command.split()
         #create tuple of common music words
         music=('music','play music','song', 'play some music')
         mus =any(elem in command  for elem in music)
         #create tuple of common stop words
         quit=('quit','stop','off','turn off','quit','power off','power')
         qu =any(elem in command  for elem in quit)
          #create tuple of common school words
         school=('school','my courses', 'homework','siu','s','i','u','work','university','college')
         learn =any(elem in command  for elem in school)
         ###create tuple of schedule like words
         calendar=('calandar','date','day','month','year', 'my schedule', 'schedule')

         #create tuple of translate like words
         translate=('translate','translate this','translation')
         trans =any(elem in command  for elem in translate)
         # if the command is in one of the tuples do certain things


         if mus:
             self.speak('playing some music for you ' + self.name)
             playsound('/home/morty/hoshi/baby_shark.mp3')
         elif learn:
             self.speak('checking my courses ')
             webbrowser.open("https://mycourses.siu.edu/d2l/login")
         elif qu:
             self.listen=False
             self.speak('Goodbye')
             os.system('killall python3')
         elif trans:
             self.speak('translating for you ' + self.name)
             self.speak('Speak after the beep')

             self.create_audio()
             self.speak('the translation is ' +self.recognize())


    ##Get Users name with Hoshi
    def get_name(self):
        new_user=('new','user','new user','new account')
        #query the database for names
        users=self.memory.get_names()
        print(users)
        #ask if that is your name
        for name in users:
            self.speak('is This ' + str(name[1]))
            answer=self.get_response()
            if answer.lower()=='yes':
                self.name=str(name[1])
                self.speak('hello' + self.name)
                break
            elif answer.lower() in new_user:
                self.speak('What is your name?')
                self.name=self.get_response()
                self.memory.insert_name(self.name)
                break

        if self.name.lower()=='new user':
            self.speak('What is your name?')
            self.name=self.get_response()
            self.memory.insert_name(self.name)

     # def __main__:
     #     self.name= input(hoshi.speak('What is your name?'))
     #     self.speak('Hello,' + self.name + ' I am Hoshi. Please Give me a command')
     #     self.speak('Say record')
