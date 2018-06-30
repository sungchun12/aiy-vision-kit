#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the buzzer button playing the FFVII Victory music while lighting up the button."""

print ('Press the button to play the theme and turn light on. It will autoplay first.')

#import packages 
from signal import pause
import threading
from threading import Thread
import math
import time
import logging

#import custom AIY packages
import aiy.toneplayer
from aiy.vision.leds import Leds
from gpiozero import Button

#setup logging features
logging.basicConfig(level=logging.INFO)
logger=logging.getLogger(__name__)

#set RGB lighting parameters
WHITE = (0xff, 0xFF, 0xFF)
BLUE = (0x00, 0x00, 0xFF)
leds=Leds()

#notation for victory fanfare music
victory_fanfare_theme= [
        'C5s',
        'C5s',
        'C5s',
        'C5rs',
        'g4q',
        'a4q',
        'C5es',
        'a4s',
        'C5rs',
    ]    

#function to make color blend the gradient from color to color
def blend(color_a, color_b, alpha):
    return tuple([math.ceil(alpha * color_a[i] + (1.0 - alpha) * color_b[i]) for i in range(3)])

#light function that lasts for set number of seconds. The longer the time, the more color gradients.
def light_on():
    for i in range(20):
        leds.update(Leds.rgb_on(blend(WHITE, BLUE, i / 20)))
        time.sleep(0.02)
        
#Set the tone player to play music notation above
def theme_on():
    player = aiy.toneplayer.TonePlayer(22)
    player.play(*victory_fanfare_theme)
    leds.reset()

#Setup the button functionality
button=Button(23) #pin 23 makes the button work on GPIO
button.when_pressed=light_on
button.when_released=theme_on

#auto-plays theme and turns light on
if __name__ == '__main__':
    Thread(target=light_on).start()
    Thread(target=theme_on).start()

#wait for user to kill example
pause()
