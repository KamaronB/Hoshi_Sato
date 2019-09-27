#!/usr/bin/env python3
from talk_to_me import Hoshi
from trans_mover import TransMover
import os
import time
import pyaudio
import numpy
import random
import uuid
import webbrowser
import pandas as pd
from hoshi_feelings import Feelings




#load classify class
feelz= Feelings('/home/morty/hoshi/HoshiFeelz2.pickle')

#new classifier instance
# trans= TransMover('/home/morty/hoshi')
# print(trans.translate("yes"))


# webbrowser.open("https://www.youtube.com/watch?v=wo1OwRTRKRk?autoplay=1")
# # os.system('rm *.wav')
hoshi= Hoshi('output.wav','/home/morty/hoshi')
cont=False
while cont==False:
    try:
        hoshi.get_name()
        cont=True
    except:
        hoshi.speak('Try again')
        print('error at getting name')
        cont = False


# hoshi.run_command('translate')

#hoshi
# hoshi.create_audio()
# hoshi.speak( 'I believe what you just said was' + hoshi.recognize())


hoshi.listening()


while hoshi.listen==True:
  left, right = hoshi.listening()
  if max(right) > hoshi.threshold and time.time() - hoshi.last_run > hoshi.min_delay:
    hoshi.speak('Did you say something?'+hoshi.name)
    response=hoshi.get_response()
    if response.lower()=='yes':
        hoshi.speak('What would you like me to do?')
        hoshi.speak('Give me a command')
        command=hoshi.get_response()
        if feelz.classify(command):
            hoshi.speak('You dont have to be rude')
            hoshi.run_command(command)
        else:
            hoshi.run_command(command)
    hoshi.last_run = time.time()
