import os
import logging
import logging.handlers
import subprocess as sp
import json


class AudioConverter:

    def __init__(self,file_name):
        self.file_name = file_name        
        self.FFMPEG_BIN = "ffmpeg"
        self.filepath, self.ext = os.path.splitext(self.file_name)

    def convert_to_mp3(self):
        """
        Converts a input file to mp3

        command: ffmpeg -n -i input.m4a -acodec libmp3lame -ab 128k output.mp3
        """
        if self.ext == ".mp3":
            return        

        codec = "libmp3lame"
        mp3_filename = self.filepath + ".mp3"

        command = [self.FFMPEG_BIN,
                   "-n",
                   "-i", self.file_name,
                   "-acodec", codec,
                   "-ab", "128k",
                   mp3_filename
                   ]
        return command

    def convert_to_ogg(self):
        """
        Converts a input file to ogg

        command: ffmpeg -n -i input.m4a -acodec libvorbis -aq 60 -vn -ac 2 output.ogg
        """
        if self.ext == ".ogg":
            return

        codec = "libvorbis"
        ogg_filename = self.filepath + ".ogg"

        command = [self.FFMPEG_BIN,
                   "-n",
                   "-i", self.file_name,
                   "-acodec", codec,
                   "-aq", "60",
                   "-vn",
                   "-ac", "2",
                   ogg_filename
                   ]

        return command


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


# Change the directory of audio files here
if __name__ == "__main__":
    # rootdir = os.getcwd()  #default:  get the current dir
    rootdir = "/home/pariwesh/audio_converter/audio_tests/"
    
    process_queue = []
    output_formats = [".mp3",".ogg"]

    all_files = []
    input_format = [".m4a",".wav"]


    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath, ext = os.path.splitext(file)
            if ext in input_format:
                path_from_root = os.path.join(subdir, file)
                file_path = os.path.realpath(path_from_root)

                try: 
                    converter = AudioConverter(file_path)
                    if ".mp3" in output_formats:
                        process_queue.append(converter.convert_to_mp3())
                    if ".ogg" in output_formats:
                        process_queue.append(converter.convert_to_ogg())
                except Exception as e:
                    print e
    
    
    try:
        log_file = open("audio_tests/audio_converter.log", 'a')
    except:
        log_file = open("audio_tests/audio_converter.log", 'w+')

    for x in range(0,2):
        for command in process_queue:
            try:
                proc = sp.Popen(command, stdout=log_file,
                            bufsize=10**8)
                del proc

            except IOError as e:
                log_file.write(str(e))
            except Exception as e:
                log_file.write(str(e))