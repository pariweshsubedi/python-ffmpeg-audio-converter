Documentation for installation :

1) FFMPEG installation:

sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next
sudo apt-get update
sudo apt-get install ffmpeg

2) Change the value of "rootdir" from file "convert_existing.py"

3) Run the script to convert audio within the root dir

```
python convert_existing.py
```