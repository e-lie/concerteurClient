#!/usr/bin/python3

from urllib import request
import urllib
import parse
import json
import os
from glob import glob
from pydub import AudioSegment

SERVER_URL = os.environ['SERVER_URL']
SOUND_DIR = ['SOUND_DIR']
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
    with open("sounds/"+filename, 'wb') as f:
        querystring = urllib.parse.urlencode(params)
        resp = request.urlopen(url, querystring.encode('utf-8'))
        mp3 = resp.read()
        f.write(mp3)


def convert_sounds_to_wav():
    mp3_files = glob(SOUND_DIR+"*.mp3")
    for mp3 in mp3_files:
        mp3seg = AudioSegment.from_mp3(mp3)
        mp3seg.export(mp3.replace('.mp3','.wav'), format="mp3")

def write_sound_list():
    with open(SOUND_DIR+"sound_list.txt", 'wt') as f:
        wav_files = glob(SOUND_DIR+"*.wav")
        #to sort files by their id keep only the filename
        sortkey = lambda filename: int(parse.parse("{}_{}_{}",
                                        filename.replace(SOUND_DIR,''))[0])
        wav_files.sort(key = sortkey)
        i = 0
        mode = "w"
        for wav in wav_files:
            if i>0:
                mode = "a"
            with open(SOUND_DIR+"sound_list.txt",mode) as f:
                f.write("{} {};\n".format(i,wav))
            i+=1

        with open(SOUND_DIR+"params.txt",'w') as f:
            f.write("{} {};\n".format('file_count',i))

if __name__ == "__main__":
    data = get_sound_list()
    soundList = data['filenames']
    lastFilename = data['lastfilename']
    for sound in soundList:
        get_sound(sound)
    with open('last_file_name.txt','w') as f:
        f.write(lastFilename)

    convert_sounds_to_wav(SOUND_DIR)
    write_sound_list(SOUND_DIR)
