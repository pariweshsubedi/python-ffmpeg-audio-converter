import subprocess as sp
import os
import sys
from datetime import datetime

class AudioConverter:
    def __init__(self,file_name):
        self.file_name = file_name
        self.FFMPEG_BIN = "ffmpeg"
        
    
    def _render_error(self,msg):
        print msg
        return

    def convert_to_mp3(self):
        """
        @param : 
            file: file name that is to be converted to mp3

        command: ffmpeg -i input.m4a -acodec libmp3lame -ab 128k output.mp3
        """
        if self.file_name.split(".")[1] == "mp3":
            return

        codec = "libmp3lame"
        try:
            mp3_filename = self.file_name.split(".")[0] + ".mp3"
        except:
            self._render_error("Error while processing file name")
            return 

        command = [self.FFMPEG_BIN,
                    "-i",self.file_name,
                    "-acodec",codec,
                    "-ab", "128k",
                    mp3_filename
                    ]

        return self._convert(command)

    def convert_to_ogg(self):
        """
        @param : 
            file: file name that is to be converted to ogg
        
        command: ffmpeg -i input.m4a -acodec libvorbis -aq 60 -vn -ac 2 output.ogg
        """
        if self.file_name.split(".")[1] == "ogg":
            return

        codec = "libvorbis"        

        try:
            ogg_filename = self.file_name.split(".")[0] + ".ogg"
        except:
            self._render_error("Error while processing file name")
            return 

        command = [self.FFMPEG_BIN,
                        "-i",self.file_name,
                        "-acodec",codec,
                        "-aq", "60",
                        "-vn",
                        "-ac", "2",
                        ogg_filename
                    ]

        return self._convert(command)




    def _convert(self,command,logfile=True):
        """
        @param:
            command: command for conversion
        """

        if logfile:
            try:
                log_file = open("audio-converter-api.log", 'a')
            except:
                log_file = open("audio-converter-api.log", 'w+')

        proc = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8, stderr=log_file)
        if proc.returncode:
            err = "\n".join(["Running test: %s\n" % cmd,
            "WARNING: this command returned an error:",
            err.decode('utf8')])
            
            raise IOError(err)

        del proc


"""
Local Testing:
    - place this file to the folder with the audio files or
      just change the _dir variable to the directory with audio files to test
"""
if __name__ == "__main__":

    output_formats = ["mp3","ogg"]

    _dir = os.getcwd()  #default:  get the current dir

    files = []
    input_format = ["mp3","m4a","ogg","wav"]
    
    for f in os.listdir(_dir):
        try:
            if f.split(".")[1] in input_format:
                files.append(f)
        except:
            pass


    for f in files:
        t1 = datetime.now()
        converter = AudioConverter(f)
        if "mp3" in output_formats:
            converter.convert_to_mp3()
        t2 = datetime.now()
        if "ogg" in output_formats:
            converter.convert_to_ogg()
        t3 = datetime.now()

        print "Time to convert {0} to mp3 : {1}".format(f,t2-t1)
        print "Time to convert {0} to ogg : {1}".format(f,t3-t2)
        print " "