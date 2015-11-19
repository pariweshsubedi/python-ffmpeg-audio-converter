from flask import Flask, request, make_response, jsonify, redirect, url_for
import logging,os
from logging.handlers import RotatingFileHandler
from audio_converter import AudioConverter

app = Flask(__name__)
app.config.from_pyfile('settings.py')

@app.errorhandler(400)
def bad_request(error):
    app.logger.error('400')
    return make_response(jsonify({"Response":"Bad request"}), 400)

@app.errorhandler(405)
def request_not_allowed(error):
    app.logger.error('405')
    return make_response(jsonify({"Response":"Not allowed"}), 405)

@app.errorhandler(500)
def server_error(error):
    app.logger.error('500')
    return make_response(jsonify({"Response":"Internal server error"}), 500)

@app.errorhandler(404)
def not_found(error):
    app.logger.error('404')
    return make_response(jsonify({"Response":"Not found"}), 404)

@app.route('/', methods=['GET'])
def index():
    app.logger.warning('Index hit. Crawler? Check IP: {0}'.format(request.remote_addr))
    return make_response(jsonify({"Response":"api index"}), 200)

@app.route('/convert', methods=['POST'])
def convert_audio():
	"""
	Convert a audio RotatingFileHandler
	@param: 
		file : (string) name of the file to for audio conversion
	"""

	# try: 
	data = request.get_json()

	try:
		filename = data['filename']
	except (KeyError, TypeError):
		app.logger.error('Keys not present in request')
		return redirect(url_for('bad_request'))

	_dir = os.getcwd() + "/audio_tests"

	files = []
	files_audio_format = ["mp3","m4a","ogg","wav"]
	files_in_dir = os.listdir(_dir)

	if filename in files_in_dir:
		if filename.split(".")[1] in files_audio_format:
			converter = AudioConverter(_dir+"/"+filename)				
			converter.convert_to_mp3()
			converter.convert_to_ogg()
		else:
			return make_response(jsonify({"success":False,"message":"incorrect file format"}), 200)
	else:
		return make_response(jsonify({"success":False,"message":"File not found"}), 200)


	# except:
	# 	return redirect(url_for('request_not_allowed'))

	return make_response(jsonify({"Response":"api index"}), 200)

if __name__ == "__main__":
    app.run()