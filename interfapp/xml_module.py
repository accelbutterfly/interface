import argparse #to get the file name from the args
from pydub import AudioSegment
from pydub.silence import split_on_silence
import speech_recognition as sr
from textblob import TextBlob
import os

#################### Parse args from the command line ####################  
#parser = argparse.ArgumentParser()
#parser.add_argument("myFile", type=str, help="The file that have to be converted to xml. Either txt or wav.")
#args = parser.parse_args()
#file_to_translate = args.myFile
#f_type = file_to_translate[-3:]

#class FileException(Exception):
#    pass

#if f_type not in  ("wav","txt"):
#    raise FileException("Invalid file type")

##################### Translate .wav to .txt ################### 
def wav_to_txt(file_to_translate):
    print("\nConverting",file_to_translate,"into .txt...")
    sound_file = AudioSegment.from_wav(file_to_translate)

    #detect silences to break sound file into different sentences
    envDB = sound_file[:150].dBFS
    print(envDB)
    audio_chunks = split_on_silence(sound_file,
         # must be silent for this time in ms :
         min_silence_len=500,
         keep_silence=200,
         # consider it silent if quieter than this dBFS :
         silence_thresh=envDB+5
    )

    chunks = []

    # Export the chunks as wav files
    for i, chunk in enumerate(audio_chunks):
        out_file = "voicetotxtchunk{0}.wav".format(i)
        print("exporting", out_file)
        chunk.export(out_file, format="wav")
        chunks.append(out_file)

    #Recognise the speech in each chunk = each sentence

    def decodeSpeech(wavefile):
        r = sr.Recognizer()
        with sr.WavFile(wavefile) as source:
            audio = r.record(source)
            try:
                return r.recognize_google(audio, language='fr-FR', show_all=False)
            except LookupError:
                return('I cannot understand audio!')

    speech = ""

    for c in chunks :
        sentence = decodeSpeech(c)
        speech = speech + sentence + ".\n"
        os.remove(c)

    text_file = open(file_to_translate.split('.')[0]+".txt","w")
    text_file.write(speech)
    #file_to_translate = "translated_text.txt" 


#################### TXT TO XML ####################
def recup(partSentence) :
        return " ".join([e[0] for e in partSentence])

def scan(tags,struct) :
    for i in range(len(tags) - len(struct) + 1):
        if struct == tags[i:i+len(struct)] : return True,i,i+len(struct)
    return False, -1, -1


def txt_to_xml(file_to_translate) :
    print("\nTranslating",file_to_translate,"into .xml")
    text_file = open(file_to_translate,"r")
    speech = text_file.read()

    dict = {}
    complexStructures = [
    ["IN","PRP","VBD","JJ"],
    ["IN","PRP","VBD"],
    ["IN","PRP","VBD","VB"],
    ["IN","PRP","VBP"],
    ["IN","PRP","VBD","VBN"],
    ["IN","PRP","VBD","RB","VBN"],
    ["IN","PRP","VBD","RB","VB"],

    ["IN","PRP","MD","VBN"],
    ["IN","PRP","VBP","RB","VB"],
    ["IN","PRP","VBP","TO","VB","PRP"],
    ["IN","PRP","VBP","TO","VB","PRP","RB"],
    ["IN","PRP","VBP","TO","VB","RB"],
    ["IN","PRP","VBP","TO","VB"],
    ["IN","PRP","VBP","TO","PRP"],
    ["IN","PRP","VBP","TO","PRP","RB","JJ"],
    ["IN","PRP","VBP","TO","PRP"],

    ["IN","DT","NN","VBZ","RB","JJ"]
    ]
    keywordsTags = (
    ["NN"], ["NNS"],["NNP"],["NNPS"],["FW"],["PRP"],["STRUCT"],["JJ"],["JJR"],["JJS"])
    # The type of words that will be considered as nodes
    # If they are not in keywords and encounter the same word twice, there will be 2 different nodes
    nodeWordsTags = keywordsTags
    verbTags = ("VB","VBD","VBN","VBP","VBZ")
    withVerbTags = ("RB","RBR","RBS","CC")

    complexStructures.sort(key = lambda x : -len(x))

    nodes = []
    edges = []

    sentences = [TextBlob(s).tags for s in speech.split(".") if s.strip()!=""]
    print("\nSpeech :\n"+speech,"\n")

    for taggedSentence in sentences :
        #print("Tagged sentence :",taggedSentence)
        tags = [e[1] for e in taggedSentence]
        buff = ""
        lastSubject = -1
        # Are there complex structures ?
        for s in complexStructures :
            bool, i, j = scan(tags,s)
            while bool :
                print()
                taggedSentence = taggedSentence[0:i]+[[recup(taggedSentence[i:j]),"STRUCT"]]+taggedSentence[j:]
                tags = [e[1] for e in taggedSentence]
                bool, i, j = scan(tags,s)
        for taggedWord in taggedSentence :
            if [taggedWord[1]] in nodeWordsTags :
                if lastSubject == -1 and buff!="":
                    nodes.append([len(nodes),' '])
                    lastSubject = len(nodes)-1
                if [taggedWord[1]] in keywordsTags :
                    word=taggedWord[0].lower() if taggedWord[1]!="NNP" else taggedWord[0]
                    if word in dict :
                        currentID = dict[word]
                    else :
                        dict[word] = len(nodes)
                        nodes.append([len(nodes),word])
                        currentID = len(nodes)-1
                else :# not a keyword but a node word
                    currentID = len(nodes)
                    nodes.append([currentID,word])

                edges.append([lastSubject,currentID,buff if buff!='' else " "])
                lastSubject = currentID
                buff = ""
            else :
                buff += ' '+taggedWord[0]
        if buff != "" :
            currentID = len(nodes)
            nodes.append([currentID,"."])
            edges.append([lastSubject,currentID,buff])

    print("Nodes :",nodes)
    print("Edges :",edges)
    print("\n")
    # Transform the lists nodes and edges into xml for js vizualisation

    fh = open(file_to_translate.split('.')[0]+".xml","w")
    fh.write("<graph>\n")
    for n in nodes :
            fh.write("<node id='"+str(n[0])+"'>"+n[1]+"</node>\n")
    for e in edges :
        if e[0]!=-1 and e[1]!=-1 and e[2]!="" :
            fh.write("<edge begin='"+str(e[0])+"' target='"+str(e[1])+"'>"+e[2]+"</edge>\n")
    fh.write("</graph>")
    fh.close()

    print("XML file : written !\n")
