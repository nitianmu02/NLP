# used for test demo

import requests
import hashlib
from .latent_glat.fairseq.fairseq_cli.infer import cli_main, infer_step, main_setting
import time
import nltk
import jieba
import subprocess
# url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
# appid = "20230424001654753"
# salt = '42'
# key = 'egbame2d6QRlW362pFjQ'
my_args = cli_main()
task, max_positions, src_dict, align_dict, tgt_dict, bpe, tokenizer, generator, models = main_setting(my_args)

def segment_string(input_string):
    # 使用 jieba 分词将输入字符串进行分词
    segmented_words = jieba.cut(input_string)
    # 将分词结果用空格连接成一个字符串
    segmented_string = " ".join(segmented_words)
    return segmented_string

def translate(text, target_lang):
    
    # md5 = hashlib.md5()
    # sign = appid + text + salt + key
    # sign = sign.encode('utf-8')
    # md5.update(sign)
    # sign = md5.hexdigest()
    #
    # params = {
    #     "q": text,
    #     "from": "auto",
    #     "to": target_lang,
    #     "appid": appid,
    #     "salt": salt,
    #     "sign": sign
    # }
    #
    # response = requests.get(url, params=params)
    #
    # result = response.json()
    # if "trans_result" in result.keys():
    #     return result["trans_result"][0]["dst"]
    # else:
    #     return ''
    print(text)

    # res = translate(words, 'en')
    # 调用 tokenizer 工具
    input_str = text
    source_lang = 'zh' if target_lang == 'en' else 'en'
    # tok
    tokenizer_cmd = [
        'latent_glat/mosesdecoder/scripts/tokenizer/tokenizer.perl', '-l',
        source_lang]  # 替换 <lang> 为输入文本的语言
    p_tok = subprocess.Popen(tokenizer_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # bpe
    bpe_model_file = "latent_glat/models/bpecode."+source_lang  # 替换为 BPE 模型文件路径
    bpe_encode_cmd = ['subword-nmt', 'apply-bpe', '-c', bpe_model_file]
    p_bpe = subprocess.Popen(bpe_encode_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    # 获取 BPE 模型的词汇表
    bpe_model_file = "latent_glat/models/bpecode." + target_lang  # 替换为 BPE 模型文件路径
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
        './latent_glat/mosesdecoder/scripts/tokenizer/detokenizer.perl',
        '-l',
        target_lang]  # 替换 <lang> 为分词后的文本的语言
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
