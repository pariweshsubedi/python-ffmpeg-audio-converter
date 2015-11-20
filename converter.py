#!/usr/bin/env python
import os
import time
import json
import logging
import logging.handlers
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess as sp


class AudioCreatedHandler(FileSystemEventHandler):
    """
    fires an event when an audio is created
    inside the working (sub)directory.
    """
    def __init__(self):
        self.FFMPEG_BIN = "ffmpeg"

    def convert_to_mp3(self,path, filename):
        """
        Converts a input file to mp3

        command: ffmpeg -i input.m4a -acodec libmp3lame -ab 128k output.mp3
        """

        codec = "libmp3lame"
        mp3_filename = filename + ".mp3"

        command = [self.FFMPEG_BIN,
                   "-i", path,
                   "-acodec", codec,
                   "-ab", "128k",
                   mp3_filename
                   ]

        return self._convert(command)

    def convert_to_ogg(self, path, filename):
        """
        Converts a input file to ogg

        command: ffmpeg -i input.m4a -acodec libvorbis -aq 60 -vn -ac 2 output.ogg
        """

        codec = "libvorbis"
        ogg_filename = filename + ".ogg"

        command = [self.FFMPEG_BIN,
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
            time.sleep(1)
            proc = sp.Popen(command, stdout=sp.PIPE,
                            bufsize=10**8)
            if proc.returncode:
                err = "\n".join(["Audio conversion: %s\n" % cmd,
                "WARNING: this command returned an error:",
                err.decode('utf8')])
                raise IOError(err)

            del proc
        except IOError as e:
            logger.error('{0}'.format(e), exc_info=True)      
    
    def on_created(self, event):
        
        """
        Runs when file is created.
        In this case, we create .mp3 and .ogg file.
        """
        extensions_watched = [".m4a", ".wav"]
        
        if event.is_directory:
            return
        
        filepath, ext = os.path.splitext(event.src_path) 

        if ext in extensions_watched:
            self.convert_to_mp3(event.src_path,filepath)
            self.convert_to_ogg(event.src_path,filepath)

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
        main(config['dir_to_watch'])
        
        #for test purposes use ./ as dir_to_watch
        #main('./')
    except Exception as e:
        print e