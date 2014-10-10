#!/usr/bin/env python

from gmusicapi import Musicmanager
from gmusicapi import Mobileclient
import pyglet
import pygame
import os
import json
from random import shuffle
import threading
import pickle

skip = False
pause = False
play = False
quit = False

try:
    os.remove("*.mp3")
except:
    clean = True

print "Logging In..."
mm = Musicmanager()
#mm.perform_oauth()
login = mm.login()

#print "Getting Songs"
#library = mm.get_uploaded_songs()
#with open('library.txt','w') as f:
#    pickle.dump( library, f)

print "Loading Library..."
with open('library.txt','r') as f:
    library = pickle.load( f )

print "Shuffling Library..."
#shuffle(library)

pygame.mixer.init()

print "Starting Playback..."
for song in library:

#    if 'Trees' not in song['artist']:
 #      continue
    if 'Everything Will' not in song['album']:
        continue

    filename, audio = mm.download_song(song['id'])
   
    with open(filename, 'wb') as f:
        f.write(audio)
    print "Playing: " + filename

#    kethread = KeyEventThread()
#    kethread.start()

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy()==True:
        if skip==True:
            skip = False
            print "Skipping..."
            break
        if quit==True:
            break
        continue

    os.remove(filename)

    if quit==True:
        break


