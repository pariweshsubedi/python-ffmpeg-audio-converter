FFMPEG python wrapper
--------------------

A simple ffmpeg wrapper to convert Audio to mp3 or ogg whenever a new file is added to the watched directory.


Installation :
---------------

1) FFMPEG installation:
	
	sudo add-apt-repository ppa:kirillshkrogalev/ffmpeg-next
	sudo apt-get update
	sudo apt-get install ffmpeg



To convert existing files:
--------------------------

1) Change the value of "dir_to_watch" from "settings.json"

2) Run the script to convert audio within the root dir


		python convert_existing.py


To start a watch process:

1) Single thread to handle all your conversions.


		python converter.py


2) Dual threads to handle mp3 and ogg conversion at a same time for a single file.

     	python multi.py 


Supervisor conf file
----------------------

	[program:audio_converter]
	command=python [script name]
	directory=[script directory]
	user=[username]
	numprocs=1
	stdout_logfile= [log file]
	stderr_logfile= [log file]
	autostart=true
	autorestart=true
	startsecs=10
	; Need to wait for currently executing tasks to finish at shutdown.
	; Increase this if you have very long running tasks.
	stopwaitsecs = 600
	; When resorting to send SIGKILL to the program to terminate it
	; send SIGKILL to its whole process group instead,
	; taking care of its children as well.
	killasgroup=true
	; if rabbitmq is supervised, set its priority higher
	; so it starts first
	priority=998

