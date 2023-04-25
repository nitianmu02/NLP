from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pysbd
from deepmultilingualpunctuation import PunctuationModel
from .translate import translate
import threading
import time
import nltk

# The default language is 'english'
# Create your views here.
seg_chn = pysbd.Segmenter(language="zh", clean=True)
seg_eng = pysbd.Segmenter(language="en", clean=True)
punc = PunctuationModel()
buf = []

time_out_counter = 0

def translate_thread():
    global buf, time_out_counter
    send = ''
    while True:
        if buf:
            print("buf:", buf)
            snt = ' '.join(buf)
            snt = punc.restore_punctuation(snt)
            print("sentence:", snt)
            seg = seg_eng.segment(snt)
            print("sbd:", seg)
            if len(seg) > 1 or time_out_counter > 3 and len(seg) > 0:
                send = seg.pop(0)
                n_words = len(nltk.word_tokenize(send)) # 使用nltk分词
                while buf and n_words > 0:
                    buf.pop(0)
                    n_words -= 1
            if send:
                res = translate(send, 'en')
                print("response:", res)
        print('-----------------------------------------')
        time.sleep(1)
        time_out_counter += 1

# translator = threading.Thread(target=translate_thread, daemon=True)
# print('start translator')
# translator.start()

@api_view(['POST'])
def speech(request):
    global buf, time_out_counter
    word = request.data.get('word')
    buf.append(word)
    send = ''
    if buf:
        print("buf:", buf)
        snt = ''.join(buf)
        snt = punc.restore_punctuation(snt)
        print("sentence:", snt)
        seg = seg_chn.segment(snt)
        print("sbd:", seg)
        if len(seg) > 1 or time_out_counter > 3 and len(seg) > 0:
            send = seg.pop(0)
            n_words = len(nltk.word_tokenize(send)) # 使用nltk分词
            while buf and n_words > 0:
                buf.pop(0)
                n_words -= 1
        if send:
            res = translate(send, 'en')
            print("response:", res)
            return Response(res)
    return Response('')