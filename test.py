import os
from audio_converter import AudioConverter

# Directory where the audio is in
_dir = os.getcwd() + "/audio_tests"

# output format
convert_to = ["mp3","ogg"]

# input file format
files_audio_format = ["m4a"]

_dir = os.getcwd()
files = []

for f in os.listdir(_dir):
        try:
            if f.split(".")[1] in files_audio_format:
                files.append(f)
        except:
            pass

    for f in files:
        converter = AudioConverter(f)
        if "mp3" in convert_to:
            converter.convert_to_mp3()
        if "ogg" in convert_to:
            convert_to.convert_to_ogg()   