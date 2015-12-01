#!/usr/bin/env python
import os
import time
import json
import logging
import logging.handlers
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess as sp
from multiprocessing.pool import ThreadPool
import multiprocessing as mp
from multiprocessing.dummy import Pool
from Queue import Queue, Empty

class AudioCreatedHandler(FileSystemEventHandler):
    """
    fires an event when an audio is created
    inside the working (sub)directory.
    """
    def __init__(self):
        self.FFMPEG_BIN = "ffmpeg"
        num = None # set to the number of workers (defaults to the cpu count of the machine)
        # files_to_convert : 1 file = 2 conversion process
        self.files_to_convert = 1
        self.lock = False
        
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

    def _convert(self, command, logfile=True):
        """
        @param:
            command: command for conversion
        """
        if logfile:
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)
            handler = logging.handlers.RotatingFileHandler(filename='requests.log', maxBytes=1024, backupCount=10)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        try:
            proc = sp.Popen(command, stdout=sp.PIPE,
                            bufsize=10**8)
            return proc
        except IOError as e:
            logger.error('{0}'.format(e), exc_info=True)      
            return None
    
    def on_created(self, event):
        
        """
        Runs when file is created.
        In this case, we create .mp3 and .ogg file.
        """
        extensions_watched = [".m4a", ".wav"]
        
        if event.is_directory:
            return
        
        self.q.put(event.src_path)

        # q is the file to convert
        while not self.q.empty():
            processes = []
            
            try:
                # for i in range(0,self.files_to_convert):
                file_src = self.q.get()
                filepath, ext = os.path.splitext(file_src)
                print "==========="
                print ext
                print "==========="
                if ext not in [".ogg",".mp3"]:
                    if ext != ".mp3":
                        p1 = self.convert_to_mp3(file_src,filepath)
                        if p1:
                            processes.append(p1)
                    if ext != ".ogg":
                        p2 = self.convert_to_ogg(file_src,filepath)
                        if p2:
                            processes.append(p2)

                print "----------------"
                print "total processes"
                print len(processes)
                print "----------------"

                for p in processes:
                    p.wait()
                    del p

            except Empty:
                print "no files to convert"
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
        print "Watching: %s" % config['dir_to_watch']
        # main(config['dir_to_watch'])
        
        #for test purposes use ./ as dir_to_watch
        main('audio_tests')
    except Exception as e:
        print e