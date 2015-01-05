#!/usr/bin/env python

from gmusicapi import Musicmanager
import pygame
import os
from random import shuffle
import threading
import pickle
import argparse
import signal
import sys
import threading
import time

skip = False
pause = False
play = False
quit = False

def exit_cleanly(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)

    print "Cleaning Up..."
    try:
        os.remove("*.mp3")
    except:
        clean = True
    sys.exit(1)

class PlayThread(threading.Thread):

    def __init__(self, mm, playlist):
        threading.Thread.__init__(self)
        self.playlist = playlist
        self.mm = mm
        pygame.mixer.init()

    def run(self):
        global skip
        global quit

        print "Starting Playback..."
        for song in playlist:

            filename, audio = self.mm.download_song(song['id'])
   
	    safe_filename = filename.replace(' ', '_')
            with open(safe_filename, 'wb') as f:
                f.write(audio)
            print "Playing: " + filename

            pygame.mixer.music.load(safe_filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy()==True:
                if skip==True:
                    skip = False
                    print "Skipping..."
                    break
                if quit==True:
                    break
                continue

            os.remove(safe_filename)

            if quit==True:
                break



if __name__ == '__main__':

    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_cleanly)


    parser = argparse.ArgumentParser(description="Google Music Player")
    parser.add_argument('-l','--login', required=False, help='Create login credentials.', action="store_true")
    parser.add_argument('-s','--shuffle', required=False, help='Play in random order.', action="store_true")
    parser.add_argument('-r', '--refresh', required=False, help='Refresh Library.', action="store_true")
    parser.add_argument('-d', '--display', required=False, help='Display playlist only.', action="store_true")
    parser.add_argument('-t', '--artist', required=False, help='Artist Filter' )
    args = parser.parse_args()    

    mm = Musicmanager()
    if args.login:
        mm.perform_oath()
        sys.exit(0)

    print "Logging In..."
    mm.login()

    if args.refresh:
        print "Getting Songs"
        library = mm.get_uploaded_songs()
        with open('library.txt','w') as f:
            pickle.dump( library, f)

    print "Loading Library..."
    with open('library.txt','r') as f:
        library = pickle.load( f )

    # Create playlist
    playlist = []
    for song in library:
        if args.artist:
            if args.artist.lower() not in song['artist'].lower():
                continue

        playlist.append( song )

    if args.shuffle:
        print "Shuffling Library..."
        shuffle(playlist)

    if args.display:
        for song in playlist:
            print "%s: %s" % ( song['artist'], song['title'])
        sys.exit(0)

    t = PlayThread( mm, playlist )
    t.daemon = True
    t.start()

    while True:
        time.sleep( 1 )
        if quit:
            break



