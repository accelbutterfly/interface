import argparse #to get the file name from the args
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from textblob import Textblob

#################### Additionnal functions ###################

def decodeSpeech(wavefile):
    r = sr.Recognizer()
    with sr.WavFile(wavefile) as source:
        audio = r.record(source)
        try :
            return r.recognise_google(audio, language='fr-FR', show_all=False)
        except LookupError:
            return('I cannot understand audio !')

def recup(partSentence):
    return " ".join([e[0] for e in partSentence])

def scan(tag, struct):
    for i in range(len(tags) - len(struct) + 1):
        if struct == tags[i:i+len(struct)] : return True, i, i+len(struct)
    return False, -1, -1

#################### True fonctions ####################

def file_to_txt(fname) :

