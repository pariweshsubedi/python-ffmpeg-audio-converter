#!/usr/bin/env python
import os
import time
import json
import logging
import logging.handlers
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess as sp
from Queue import Queue, Empty

class AudioCreatedHandler(FileSystemEventHandler):
    """
    fires an event when an audio is created
    inside the working (sub)directory.
    """
    def __init__(self):
        self.FFMPEG_BIN = "ffmpeg"
        self.q = Queue() #file queue
        

    def convert_to_mp3(self,path, filename):
        """
        Converts a input file to mp3

        command: ffmpeg -n -i input.m4a -acodec libmp3lame -ab 128k output.mp3
        """

        codec = "libmp3lame"
        mp3_filename = filename + ".mp3"

        command = [self.FFMPEG_BIN,
                   "-n",
                   "-i", path,
                   "-acodec", codec,
                   "-ab", "128k",
                   mp3_filename
                   ]

        return self._convert(command)

    def convert_to_ogg(self, path, filename):
        """
        Converts a input file to ogg

        command: ffmpeg -n -i input.m4a -acodec libvorbis -aq 60 -vn -ac 2 output.ogg
        """

        codec = "libvorbis"
        ogg_filename = filename + ".ogg"

        command = [self.FFMPEG_BIN,
                   "-n",
                   "-i", path,
                   "-acodec", codec,
                   "-aq", "60",
                   "-vn",
                   "-ac", "2",
                   ogg_filename
                   ]

        return self._convert(command)

    def _convert(self, command):
        """
        @param:
            command: command for conversion

        returns a subprocess
        """
        try:
            proc = sp.Popen(command, stdout=sp.PIPE,
                            bufsize=10**8)
            return proc
        except IOError as e:
            print e
            return None
    
    def on_created(self, event):
        """
        Runs when file is created.
        In this case, we create .mp3 and .ogg file.
        """
        
        if event.is_directory:
            return
        
        self.q.put(event.src_path)

        while not self.q.empty():
            processes = []
            try:
                file_src = self.q.get()
                filepath, ext = os.path.splitext(file_src)

                if ext not in [".ogg",".mp3",".png"]:
                    p1 = self.convert_to_mp3(file_src,filepath)
                    if p1:
                        processes.append(p1)
                    
                    p2 = self.convert_to_ogg(file_src,filepath)
                    if p2:
                        processes.append(p2)

                for p in processes:
                    p.wait()
                    del p

            except Empty:
                print "empty queue get called"
                time.sleep(1)
        return


def load_config(config_file):
    """
    load the configuration from JSON file.
    """
    try:
        with open('settings.json', 'r') as f:
            return json.loads(f.read())
    except (IOError, Exception) as e:
        print '%s' % e
        exit()


def main(dir_to_watch):
    """
    runs the observer 
    in the directory we want to watch
    
    params:
    
    dir_to_watch = (string) the directory watched.
    """
    event_handler = AudioCreatedHandler()
    observer = Observer()
    observer.schedule(event_handler, dir_to_watch, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)  
    except KeyboardInterrupt:
        print "Stopping..."
        observer.stop()
    observer.join()


if __name__ == "__main__":
    
    config = load_config('settings.json')
    try:
        main(config['dir_to_watch'])
        
        #for test purposes use ./ as dir_to_watch
        # main('audio_tests')
    except Exception as e:
        print e