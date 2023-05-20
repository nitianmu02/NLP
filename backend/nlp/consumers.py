from channels.generic.websocket import AsyncWebsocketConsumer
import json
from nlp import main
import pysbd
from deepmultilingualpunctuation import PunctuationModel
from .translate import translate
import threading
import time
import nltk
import spacy
import predictor

seg_chn = pysbd.Segmenter(language="zh", clean=False)
seg_eng = pysbd.Segmenter(language="en", clean=False)
buf = []
nlp = spacy.blank('zh')
nlp.add_pipe('sentencizer')
punc = PunctuationModel()
time_out_counter = 0

class SpeechConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Print the received text_data
        data = json.loads(text_data)
        words = data.get('words')
        print("frontend:", words)
        buf.append(words)
        main.buf.append(words)
        if words:
            await self.send_message(words)

    async def send_message(self, message):
        # Send a message to the WebSocket connection
        await self.send(json.dumps({
            'message': message
        }))

def translate_thread():
    global buf, time_out_counter
    send = ''
    while True:
        if buf:
            print("buf:", buf)
            snt = ' '.join(buf)
            # snt = punc.restore_punc(snt)
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

def sbd(buf, lang):
    if lang == 'zh':
        snt = ''.join(buf)
    elif lang == 'en':
        snt = ' '.join(buf)
        snt = punc.restore_punc(snt)
        seg = seg_eng.segment(snt)
        seg = nlp(snt)
        seg = [sent.text for sent in seg.sents]
        return seg
    
# sc = SpeechConsumer()
translator = threading.Thread(target=translate_thread, daemon=True)
print('start translator')
translator.start()