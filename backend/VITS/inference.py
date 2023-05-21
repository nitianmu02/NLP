from pathlib import Path
BASE_DIR = f'{Path(__file__).resolve().parent.parent}'
import IPython.display as ipd
import torch
import commons
import utils
from VITS.models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import soundfile as sf
import os
from scipy.io.wavfile import read
import numpy as np
import data_utils
root_dir = os.path.dirname(os.path.realpath(__file__))
def load_wav_to_torch(full_path):
    sampling_rate, data = read(full_path)
    return torch.FloatTensor(data.astype(np.float32)), sampling_rate

def spectrogram_torch(y, n_fft, sampling_rate, hop_size, win_size, center=False):
    hann_window = {}
    dtype_device = str(y.dtype) + '_' + str(y.device)
    wnsize_dtype_device = str(win_size) + '_' + dtype_device
    if wnsize_dtype_device not in hann_window:
        hann_window[wnsize_dtype_device] = torch.hann_window(win_size).to(dtype=y.dtype, device=y.device)
    y = torch.nn.functional.pad(y.unsqueeze(1), (int((n_fft-hop_size)/2), int((n_fft-hop_size)/2)), mode='reflect')
    y = y.squeeze(1)
    spec = torch.stft(y, n_fft, hop_length=hop_size, win_length=win_size, window=hann_window[wnsize_dtype_device],
                      center=center, pad_mode='reflect', normalized=False, onesided=True)
    spec = torch.sqrt(spec.pow(2).sum(-1) + 1e-6)
    return spec

def get_audio(filename, max_wav_value=32768.0, filter_length=1024, hop_length=256, win_length=1024):
    audio, sampling_rate = load_wav_to_torch(filename)
    audio_norm = audio / max_wav_value
    audio_norm = audio_norm.unsqueeze(0)
    spec = spectrogram_torch(audio_norm, filter_length,
        sampling_rate, hop_length, win_length,
        center=False)
    spec = torch.squeeze(spec, 0)
    spec_lengths = torch.LongTensor(1)
    spec_lengths[0] = spec.size(1)
    spec_padded = torch.FloatTensor(1, 513, spec.size(1))
    spec_padded.zero_()
    spec_padded[0, :, :spec.size(1)] = spec
    return spec_padded.cuda(), spec_lengths.cuda()

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

def init_model():
    
    hps = utils.get_hparams_from_file("./configs/genshin_base_ms.json")

    net_g = SynthesizerTrn(
        len(symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).cuda()
    _ = net_g.eval()

    _ = utils.load_checkpoint('./checkpoints/G_2036.pth', net_g, None)
    return net_g, hps

def gen_speech(text, net_g, hps, speaker='Yoimiya', speed = 1.):
    speaker_list = ['Paimon', 'Miko', 'Kazuha', 'Nahida',\
                'Hutao', 'Ayaka', 'Yoimiya', 'Ganyu',\
                'Mona', 'Ei']
    id = speaker_list.index(speaker)
    with torch.no_grad():
        stn_tst = get_text(text, hps)
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        sid = torch.LongTensor([id]).cuda()#@param {type:"longtensor", 0:9}
        audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667,\
            noise_scale_w=0.8, length_scale=speed)[0][0,0].data.cpu().float().numpy()
        ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate))
        audio_path = root_dir + f'./output/speech.wav'
        sf.write(audio_path,audio, samplerate=hps.data.sampling_rate)
        # os.system('move ./output/speech.wav ../static/')

def gen_speech_sts(audio_path, sid, tid, net_g, hps, speed = 1.):
    speaker_list = ['Paimon', 'Miko', 'Kazuha', 'Nahida',\
                'Hutao', 'Ayaka', 'Yoimiya', 'Ganyu',\
                'Mona', 'Ei']
    sid = speaker_list.index(sid)
    tid = speaker_list.index(tid)
    spec, spec_length = get_audio(audio_path)
    with torch.no_grad():
        audio = net_g.infer_sts(spec, spec_length, sid=torch.LongTensor([sid]).cuda(), tid=torch.LongTensor([tid]).cuda())[0][0,0].data.cpu().float().numpy()
        # ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate))
        # audio_path = f'./output/sts.wav'
        # sf.write(audio_path,audio,samplerate=hps.data.sampling_rate)
    return audio
        
def gen_speech_hyb(text, audio_path, src_speaker, tar_speaker, weight, net_g, hps, speed = 1.):
    speaker_list = ['Paimon', 'Miko', 'Kazuha', 'Nahida',\
                'Hutao', 'Ayaka', 'Yoimiya', 'Ganyu',\
                'Mona', 'Ei']
    sid = speaker_list.index(src_speaker)
    tid = speaker_list.index(tar_speaker)
    post_enc = net_g.enc_q    
    spec, spec_length = get_audio(audio_path)
    with torch.no_grad():
        stn_tst = get_text(text, hps)
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        y, _, _, y_mask = post_enc(spec, spec_length)
        audio = net_g.infer_hyb(x_tst, x_tst_lengths, y, y_mask, weight=weight, src_sid=torch.LongTensor([sid]).cuda(), tar_sid=torch.LongTensor([tid]).cuda())[0,0].data.cpu().float().numpy()
        ipd.display(ipd.Audio(audio, rate=hps.data.sampling_rate))  
        audio_path = f'./output/hyb.wav'
        sf.write(audio_path,audio,samplerate=hps.data.sampling_rate)
        
# net_g, hps = init_model()
# gen_speech_sts('./src/audio/4001 00150.wav', 'Miko', 'Ayaka', net_g, hps)
# gen_speech_hyb('最近八重堂穿越异世的小说也太多了，哼，就对自己的世界如此不满吗。', './src/audio/1.02.wav', 'Miko', 'Ei', 0, net_g, hps)