#!/usr/bin/python3

from urllib import request
import urllib
import parse
import json
import os
from glob import glob
from pydub import AudioSegment

SERVER_URL="http://81.67.71.234:9000"
SOUND_DIR="/home/pi/concerteurClient/sounds/"
LAST = 'last_file_name.txt'

def get_sound_list():
    #Local POST request to the flask app using a custom port
    url = SERVER_URL + '/get-sound-list'
    with open(SOUND_DIR+LAST, 'r') as f:
        filename = f.readline()
        params = {'lastFilename':filename}

        # Encode the query string
        querystring = urllib.parse.urlencode(params)

        # Make a POST request and read the response
        resp = request.urlopen(url, querystring.encode('utf-8'))
        #read bytes from the JSON response and convert it to string (decode) then dictionnary (json.loads)
        jsondata = resp.read().decode('utf-8')
        return json.loads(jsondata)
        
def get_sound(filename):
    url = SERVER_URL + '/get-sound'
    params = {'soundname':filename}
    with open(SOUND_DIR+filename, 'wb') as f:
        querystring = urllib.parse.urlencode(params)
        resp = request.urlopen(url, querystring.encode('utf-8'))
        mp3 = resp.read()
        f.write(mp3)


def convert_sounds_to_wav(new_files):
    mp3_files = glob(SOUND_DIR+'*.mp3')
    file_number = len(mp3_files) - len(new_files)
    for mp3_filename in new_files:
        file_number += 1
        mp3_path = SOUND_DIR+mp3_filename
	
        mp3seg = AudioSegment.from_mp3(mp3_path)
        mp3seg.export("{}{}.wav".format(SOUND_DIR,file_number), format="wav")
    
    with open(SOUND_DIR+'params.txt', 'w') as f:
        f.write(str(len(mp3_files)))


if __name__ == "__main__":
    data = get_sound_list()
    new_files = data['filenames']
    last_filename = data['lastfilename']
    for sound in new_files:
        get_sound(sound)
    with open(SOUND_DIR+LAST, 'w') as f:
        f.write(last_filename)

    convert_sounds_to_wav(new_files)
