from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import pysbd
from deepmultilingualpunctuation import PunctuationModel
# from .zh_punct import zh_punc
# from .translate import translate
import threading
from .latent_glat.fairseq.fairseq_cli.infer import cli_main, infer_step, main_setting
import time
import nltk
import spacy
import jieba
import subprocess


# The default language is 'english'
# Create your views here.
seg_chn = pysbd.Segmenter(language="zh", clean=False)
seg_eng = pysbd.Segmenter(language="en", clean=False)
buf = []
nlp = spacy.blank('zh')
nlp.add_pipe('sentencizer')
punc = PunctuationModel()
time_out_counter = 0
my_args = cli_main()
task, max_positions, src_dict, align_dict, tgt_dict, bpe, tokenizer, generator, models = main_setting(my_args)



def translate_thread():
    global buf, time_out_counter
    send = ''
    while True:
        if buf:
            print("buf:", buf)
            snt = ' '.join(buf)
            snt = punc.restore_punc(snt)
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
                # res = translate(send, 'en')
                res = infer_step(['我 今天 真的 是 好 开心 哦'], my_args, task, max_positions, src_dict, align_dict, tgt_dict, bpe, tokenizer,
                           generator, models)
                print("response:", res)
        print('-----------------------------------------')
        time.sleep(1)
        time_out_counter += 1

# translator = threading.Thread(target=translate_thread, daemon=True)
# print('start translator')
# translator.start()

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


def segment_string(input_string):
    # 使用 jieba 分词将输入字符串进行分词
    segmented_words = jieba.cut(input_string)
    # 将分词结果用空格连接成一个字符串
    segmented_string = " ".join(segmented_words)
    return segmented_string


def remove_consecutive_duplicates(sentence):
    words = sentence.split()  # 将句子拆分为单词列表
    result = [words[0]]  # 初始化结果列表，将第一个单词添加到结果中
    for word in words[1:]:
        if word.lower() != result[-1].lower():  # 判断当前单词（转换为小写）是否与结果列表中的最后一个单词（转换为小写）相同
            result.append(word)  # 若不相同，则将当前单词添加到结果中
    return ' '.join(result)  # 将结果列表中的单词用空格连接成字符串


@api_view(['POST'])
def speech(request):
    # global buf, time_out_counter
    words = request.data.get('words')
    if words:
        print(words)

        # res = translate(words, 'en')
        # 调用 tokenizer 工具
        input_str = words
        # tok
        tokenizer_cmd = [
            'latent_glat/mosesdecoder/scripts/tokenizer/tokenizer.perl', '-l',
            'zh']  # 替换 <lang> 为输入文本的语言
        p_tok = subprocess.Popen(tokenizer_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        # bpe
        bpe_model_file = "latent_glat/models/bpecode.zh"  # 替换为 BPE 模型文件路径
        bpe_encode_cmd = ['subword-nmt', 'apply-bpe', '-c', bpe_model_file]
        p_bpe = subprocess.Popen(bpe_encode_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

        # 获取 BPE 模型的词汇表
        bpe_model_file = "latent_glat/models/bpecode.en"  # 替换为 BPE 模型文件路径
        get_vocab_cmd = ['subword-nmt', 'get-vocab']
        with open(bpe_model_file, 'r', encoding='utf-8') as f:
            bpe_vocab = [line.split()[0] for line in f]
        get_vocab_cmd.extend(bpe_vocab)
        # 调用 get-vocab 命令获取词汇表
        p_debpe = subprocess.Popen(get_vocab_cmd, stdout=subprocess.PIPE, text=True)
        vocab_output, _ = p_debpe.communicate()
        # 将词汇表转换为字典
        bpe_dict = {}
        for idx, word in enumerate(vocab_output.strip().split('\n')):
            bpe_dict[word] = idx

        detokenizer_cmd = [
            '/Users/baowudi/Documents/NLP/backend/nlp/latent_glat/mosesdecoder/scripts/tokenizer/detokenizer.perl',
            '-l',
            'en']  # 替换 <lang> 为分词后的文本的语言
        p_detok = subprocess.Popen(detokenizer_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)


        output_str, _ = p_tok.communicate(input_str)

        # 调用 subword-nmt 进行编码
        output_str, _ = p_bpe.communicate(output_str)

        res = infer_step([segment_string(words)], my_args, task, max_positions, src_dict, align_dict, tgt_dict, bpe,
                         tokenizer, generator, models)
        # debpe
        res = ' '.join([bpe_dict.get(piece, piece) for piece in res.split()])
        # 调用 detokenizer 工具
        res, _ = p_detok.communicate(res)
        res = remove_consecutive_duplicates(res)
        print("response:", res)
        return Response(res)
    return Response('')