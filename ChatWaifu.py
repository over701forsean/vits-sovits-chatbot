from scipy.io.wavfile import write
from mel_processing import spectrogram_torch
from text import text_to_sequence, _clean_text
from models import SynthesizerTrn
import utils
import commons
import sys
import re

from torch import no_grad, LongTensor
import logging
from winsound import PlaySound

chinese_model_path = r".\model\CN\model.pth"
chinese_config_path = r".\model\CN\config.json"
japanese_model_path = r".\model\H_excluded.pth"
japanese_config_path = r".\model\config.json"
tolove_model_path = r".\model\ToLove\1113_epochs.pth"
tolove_config_path = r".\model\ToLove\config.json"
bb_model_path = r".\model\G_bb_v100_820000.pth"
bb_config_path = r".\model\bb_test.json"
####################################
#CHATGPT INITIALIZE
from pyChatGPT import ChatGPT
import json

modelmessage = """ID      Output Language
0       Chinese
1       Japanese
"""

idmessage_cn = """ID      Speaker
0       綾地寧々
1       在原七海
2       小茸
3       唐乐吟
"""

idmessage_jp = """ID      Speaker
0       綾地寧々
1       因幡めぐる
2       朝武芳乃
3       常陸茉子
4       ムラサメ
5       鞍馬小春
6       在原七海
"""
idmessage_tolove = """ID      Speaker
0       金色の闇
1       モモ
2       ナナ
3       結城美柑
4       古手川唯
5       黒咲芽亜
6       ネメシス
7       村雨静
8       セリーヌ
9       ララ
10      天条院沙姫
11      西連寺春菜
12      ルン
13      メイ
14      霧崎恭子
15      籾岡里紗
16      沢田未央
17      ティアーユ
18      九条凛
19      藤崎綾
20      結城華
21      御門涼子
22      アゼンダ
23      夕崎梨子
24      結城梨斗
25      ペケ
26      猿山ケンイチ
27      レン
28      校長
"""
def get_input():
    # prompt for input
    print("You:")
    user_input = input()
    return user_input

def get_input_jp():
    # prompt for input
    print("You:")
    user_input = input() +" 使用日本语"
    return user_input

def get_token():
    token = input("Copy your token from ChatGPT and press Enter \n")
    return token

      
################################################


logging.getLogger('numba').setLevel(logging.WARNING)


def ex_print(text, escape=False):
    if escape:
        print(text.encode('unicode_escape').decode())
    else:
        print(text)


def get_text(text, hps, cleaned=False):
    if cleaned:
        text_norm = text_to_sequence(text, hps.symbols, [])
    else:
        text_norm = text_to_sequence(text, hps.symbols, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm


def ask_if_continue():
    while True:
        answer = input('Continue? (y/n): ')
        if answer == 'y':
            break
        elif answer == 'n':
            sys.exit(0)


def print_speakers(speakers, escape=False):
    if len(speakers) > 100:
        return
    print('ID\tSpeaker')
    for id, name in enumerate(speakers):
        ex_print(str(id) + '\t' + name, escape)


def get_speaker_id(message):
    speaker_id = input(message)
    try:
        speaker_id = int(speaker_id)
    except:
        print(str(speaker_id) + ' is not a valid ID!')
        sys.exit(1)
    return speaker_id


def get_label_value(text, label, default, warning_name='value'):
    value = re.search(rf'\[{label}=(.+?)\]', text)
    if value:
        try:
            text = re.sub(rf'\[{label}=(.+?)\]', '', text, 1)
            value = float(value.group(1))
        except:
            print(f'Invalid {warning_name}!')
            sys.exit(1)
    else:
        value = default
    return value, text


def get_label(text, label):
    if f'[{label}]' in text:
        return True, text.replace(f'[{label}]', '')
    else:
        return False, text



def generateSound(inputString, id, model_id,whichmodel = 0,info = None,iname = None):
    if '--escape' in sys.argv:
        escape = True
    else:
        escape = False
    if whichmodel == 0:
        #model = input('0: Chinese')
        #config = input('Path of a config file: ')
        if model_id == 0:
            model = chinese_model_path
            config = chinese_config_path
        elif model_id == 1:
            model = japanese_model_path
            config = japanese_config_path
        elif model_id == 2:
            model = tolove_model_path
            config = tolove_config_path


        hps_ms = utils.get_hparams_from_file(config)
        n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
        n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
        emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False
        sid = info['sid']
        ssid = LongTensor(sid)
        net_g_ms = SynthesizerTrn(
            n_symbols,
            hps_ms.data.filter_length // 2 + 1,
            hps_ms.train.segment_size // hps_ms.data.hop_length,
            n_speakers=n_speakers,
            emotion_embedding=emotion_embedding,
            **hps_ms.model)
        _ = net_g_ms.eval()
        utils.load_checkpoint(model, net_g_ms)
    elif whichmodel == 1:
        hps_ms = utils.get_hparams_from_file(r'config/config.json')
        # with open("pretrained_models/info.json", "r", encoding="utf-8") as f:
        #     models_info = json.load(f)
        # for i, info in models_info.items():
        #     if not info['enable']:
        #         continue
        #     if not info['name_zh'] == cnname:
        #         continue
        ssid = LongTensor(int(info['sid']))
            # name_en = info['name_en']
            # name_zh = info['name_zh']
            # title = info['title']
            # cover = f"pretrained_models/{i}/{info['cover']}"
            # example = info['example']
        # language = info['language']
        n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
        n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
        emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False
        net_g_ms = SynthesizerTrn(
            n_symbols,
            hps_ms.data.filter_length // 2 + 1,
            hps_ms.train.segment_size // hps_ms.data.hop_length,
            n_speakers=n_speakers,
            emotion_embedding=emotion_embedding,
            **hps_ms.model)
        utils.load_checkpoint(f'pretrained_models/{iname}/{iname}.pth', net_g_ms)
    elif whichmodel == 2:
        model = bb_model_path
        config = bb_config_path
        hps_ms = utils.get_hparams_from_file(config)
        n_speakers = hps_ms.data.n_speakers if 'n_speakers' in hps_ms.data.keys() else 0
        n_symbols = len(hps_ms.symbols) if 'symbols' in hps_ms.keys() else 0
        emotion_embedding = hps_ms.data.emotion_embedding if 'emotion_embedding' in hps_ms.data.keys() else False
        ssid = LongTensor([id])
        net_g_ms = SynthesizerTrn(
            n_symbols,
            hps_ms.data.filter_length // 2 + 1,
            hps_ms.train.segment_size // hps_ms.data.hop_length,
            n_speakers=n_speakers,
            emotion_embedding=emotion_embedding,
            **hps_ms.model)
        _ = net_g_ms.eval()
        utils.load_checkpoint(model, net_g_ms)

    if n_symbols != 0:
        if not emotion_embedding:
            #while True:
            if(1 == 1):
                choice = 't'
                if choice == 't':
                    text = inputString
                    if text == '[ADVANCED]':
                        text = "我不会说"

                    length_scale, text = get_label_value(
                        text, 'LENGTH', 1, 'length scale')
                    noise_scale, text = get_label_value(
                        text, 'NOISE', 0.667, 'noise scale')
                    noise_scale_w, text = get_label_value(
                        text, 'NOISEW', 0.8, 'deviation of noise')
                    cleaned, text = get_label(text, 'CLEANED')

                    stn_tst = get_text(text, hps_ms, cleaned=cleaned)
                    
                    # speaker_id = id
                    out_path = "output.wav"

                    with no_grad():
                        x_tst = stn_tst.unsqueeze(0)
                        x_tst_lengths = LongTensor([stn_tst.size(0)])
                        sid = ssid
                        audio = net_g_ms.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=noise_scale,
                                               noise_scale_w=noise_scale_w, length_scale=length_scale)[0][0, 0].data.cpu().float().numpy()

                write(out_path, hps_ms.data.sampling_rate, audio)
                print('Successfully saved!')
                return audio

def usechatwaifu(model_id,id,message):
    # session_token = get_token()
    # api = ChatGPT(session_token)
    # print(modelmessage)
    # model_id = int(input('选择回复语言: '))
    # if model_id == 0:
    #     print("\n" + idmessage_cn)
    #     id = get_speaker_id('选择角色: ')
    # elif model_id == 1:
    #     print("\n" + idmessage_jp)
    #     id = get_speaker_id('选择角色: ')
    # print(id)
    while True:

        if model_id == 0:
            resp = message
            if(resp == "quit()"):
                break
            # answer = resp["message"].replace('\n','')
            # print("ChatGPT:")
            # print(answer)
            wav = generateSound("[ZH]"+resp+"[ZH]", id, model_id)
        elif model_id == 1:
            resp = message
            wav = generateSound(resp, id, model_id)
        elif model_id == 2:
            resp = message
            wav = generateSound(resp, id, model_id)

        # PlaySound(r'.\output.wav', flags=1)
        return wav