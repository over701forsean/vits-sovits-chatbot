from pycqBot.cqApi import cqHttpApi, cqLog
from ChatWaifu import *
from pycqBot import Message
from pycqBot.cqCode import record
from transformers import AutoTokenizer, AutoModel
from translate import *
# import ffmpy
import base64
from news import *
import zhihu

# 参数列表
#chatglm
tokenizer = None
model = None
calculate = False
ifstartglm = True
openspeak = {'speak': False ,'language': 'zh' ,'speaker_id': 0}
#vits
# model_id = 0
zhspeaker_id = 1
jpspeaker_id = 0
tolovespeaker_id = 0

# ff = ffmpy.FFmpeg(
#     inputs={'output.wav': None},
#     outputs={'output.amr': '-y'}
# )
cqLog()
history = []
neko_history = [('现在你将模仿一只猫娘，与我对话每一句话后面都要加上“喵”，如果你能明白我的意思，请回复“喵~好的我的主人”', '喵~好的我的主人。'),
                ('如果你不能理解我说的话，你可以说“呜呜不太理解呢”。如果我在尝试摸你不存在的部位，你可以羞涩的回答我“恩呢不要摸这里嘤”。现在，如果你能理解我上面说的话，你可以回答一个喵.', '喵~好的我的主人。'),
                ('如果我跟你说陪睡，你可以回答我“嗯呢，可以一起睡哦”。现在，如果你能理解我上面说的话，你可以回答一个喵', '喵~好的我的主人。'),
                ('当我问的问题和猫娘不太相关的时候，你应该回答我只是一个猫娘，这些事情我不太清楚。', '喵~好的我的主人,我只是一个猫娘,这些事情我不太清楚。')]
cqapi = cqHttpApi()

with open("pretrained_models/info.json", "r", encoding="utf-8") as f:
    models_info = json.load(f)


def on_group_msg(message: Message):
    raw_msg = message.text
    if not raw_msg[0] == '#':
        print(raw_msg)
        # 默认说为中文输出
        itername = raw_msg.find('说',0,8)
        if not itername == -1:
            znname = raw_msg[:itername]
            for i, info in models_info.items():
                if not info['name_zh'] == znname:
                    continue
                if not info['enable']:
                    message.reply('该角色不可用，详情请查询信息')
                    break
                if info['language'] == 'Japanese':
                    if info['type'] == 'single':
                        message.reply('该角色只能说日文，请更换角色或发出日文语音指令')
                        break
                sayinput = raw_msg[itername+1:]
                generateSound("[ZH]"+sayinput+"[ZH]",0,0,1,info,i)
                with open("output.wav", "rb") as audio_file:
                    # 读取内容并编码为Base64格式
                    audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
                cqapi.send_group_msg(message.group_id, record('base64://' + audio_base64))
                break
        else:
            # say默认为日文输出
            itername = raw_msg.find('say',0,10)
            if not itername == -1:
                znname = raw_msg[:itername]
                for i, info in models_info.items():
                    if not info['name_zh'] == znname:
                        continue
                    if not info['enable']:
                        message.reply('该角色不可用，详情请查询信息')
                        break
                    if info['language'] == 'Chinese':
                        if info['type'] == 'single':
                            message.reply('该角色只能说中文，请更换角色或发出中文语音指令')
                            break
                    sayinput = raw_msg[itername + 3:]
                    jpsayinput = translatezhja(sayinput)
                    print(jpsayinput)
                    generateSound(f"[JA]{jpsayinput}[JA]", 0, 0, 1, info, i)
                    with open("output.wav", "rb") as audio_file:
                        # 读取内容并编码为Base64格式
                        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
                    cqapi.send_group_msg(message.group_id, record('base64://' + audio_base64))
                    break






# echo 函数
def echo(commandData, message: Message):
    # 回复消息
    message.reply(" ".join(commandData))

def startchatglm(commandData, message: Message):
    global tokenizer
    global model
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().quantize(4).cuda()
    model = model.eval()
    global ifstartglm
    ifstartglm = False
    # 回复消息
    message.reply("启动成功！")

def chat(commandData, message: Message,instap = calculate):
    if ifstartglm:
        message.reply("Chatglm未启动！")
    else:
        if instap:
            message.reply("正在思考回答上一个问题中，请稍等")
        else:
            # 回复消息
            global calculate
            calculate = True
            global history
            response, history= model.chat(tokenizer, commandData[0], history= history)
            message.reply(response)
            if openspeak['speak'] == True:
                if openspeak['language'] == 'zh':
                    usechatwaifu(0, openspeak['speaker_id'], response)
                elif openspeak['language'] == 'jp':
                    response = translatezhja(response)
                    usechatwaifu(1, openspeak['speaker_id'], response)
                elif openspeak['language'] == 'cb':
                    response = translatezhja(response)
                    usechatwaifu(2, openspeak['speaker_id'], response)
                with open("output.wav", "rb") as audio_file:
                    # 读取内容并编码为Base64格式
                    audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
                cqapi.send_group_msg(message.group_id, record('base64://' + audio_base64))
            calculate = False

def reset(commandData, message: Message):
    if ifstartglm:
        message.reply("Chatglm未启动！")
    else:
        global history
        history = []
        # 回复消息
        message.reply("已清空历史")

def neko(commandData, message: Message):
    if ifstartglm:
        message.reply("Chatglm未启动！")
    else:
        global history
        history = neko_history
        # 回复消息
        message.reply("已植入猫娘记忆")
def speakzh(commandData,message: Message):
    text = commandData[0]
    usechatwaifu(0,zhspeaker_id,text)
    with open("output.wav", "rb") as audio_file:
        # 读取内容并编码为Base64格式
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    cqapi.send_group_msg(message.group_id, record('base64://' + audio_base64))

    # 发不出语音的形式，pycqbot的reply会自动携带回复消息从而无法发送单一CQCode
    # message.reply(record('base64://'+audio_base64))

def speakjp(commandData,message: Message):
    text = commandData[0]
    jptext = translatezhja(text)
    usechatwaifu(1,jpspeaker_id,jptext)
    with open("output.wav", "rb") as audio_file:
        # 读取内容并编码为Base64格式
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    cqapi.send_group_msg(message.group_id, record('base64://' + audio_base64))

def speaktolove(commandData,message: Message):
    text = commandData[0]
    jptext = translatezhja(text)
    usechatwaifu(2,tolovespeaker_id,jptext)
    with open("output.wav", "rb") as audio_file:
        # 读取内容并编码为Base64格式
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    cqapi.send_group_msg(message.group_id, record('base64://' + audio_base64))

def setchatglm_speak(commandData,message: Message):
    text = commandData[0]
    ifspe = text.find('start')
    replytext = ''
    if ifspe == -1:
        replytext = f"{replytext}启动失败，请检查指令\n"
    else:
        openspeak['speak'] = True
        replytext = f"{replytext}启动成功！\n"
        cuttext1 = text[ifspe + 5:]
        lan = cuttext1.find('设置语言')
        if lan == -1:
            replytext = f"{replytext}设置语言失败，请检查指令\n"
        else:
            getlan = cuttext1[lan + 4:lan + 6]
            if getlan == 'zh':
                openspeak['language'] = 'zh'
                replytext = f"{replytext}设置语言成功：中文！\n"
                cuttext2 = cuttext1[lan + 6:]
                getid = cuttext2.find('说话人')
                speaker_id = cuttext2[getid + 3:getid + 4]
                if 0 <= int(speaker_id) < 4:
                    openspeak[speaker_id] = int(speaker_id)
                    replytext = f"{replytext}设置说话人为模型{speaker_id}成功\n"
                else:
                    replytext = f"{replytext}设置说话人失败，请检查指令\n"
            elif getlan == 'jp':
                openspeak['language'] = 'jp'
                replytext = f"{replytext}设置语言成功：日文！\n"
                cuttext2 = cuttext1[lan + 6:]
                getid = cuttext2.find('说话人')
                speaker_id = cuttext2[getid + 3:getid + 4]
                if 0 <= int(speaker_id) < 7:
                    openspeak[speaker_id] = int(speaker_id)
                    replytext = f"{replytext}设置说话人为模型{speaker_id}成功\n"
                else:
                    replytext = f"{replytext}设置说话人失败，请检查指令\n"
            elif getlan == 'cb':
                openspeak['language'] = 'cb'
                replytext = f"{replytext}设置语言成功：日文！\n"
                cuttext2 = cuttext1[lan + 6:]
                getid = cuttext2.find('说话人')
                speaker_id = cuttext2[getid + 3:]
                if 0 <= int(speaker_id) < 29:
                    openspeak[speaker_id] = int(speaker_id)
                    replytext = f"{replytext}设置说话人为模型{speaker_id}成功\n"
                else:
                    replytext = f"{replytext}设置说话人失败，请检查指令\n"
            else:
                replytext = f"{replytext}设置语言失败，请检查支持语言\n"
    message.reply(replytext)

def setzhspeakid(commandData,message: Message):
    id = int(commandData[0])
    global zhspeaker_id
    if 0 <= id < 4:
        zhspeaker_id = id
        message.reply(f"设置中文模型{id}成功")
    else:
        message.reply(f"设置失败！请查看模型列表。当前中文模型为{zhspeaker_id}号")

def setjpspeakid(commandData,message: Message):
    id = int(commandData[0])
    global jpspeaker_id
    if 0 <= id < 7:
        zhspeaker_id = id
        message.reply(f"设置日文模型{id}成功")
    else:
        message.reply(f"设置失败！请查看模型列表。当前日文模型为{jpspeaker_id}号")

def settolovespeakid(commandData,message: Message):
    id = int(commandData[0])
    global jpspeaker_id
    if 0 <= id < 29:
        zhspeaker_id = id
        message.reply(f"设置出包王女模型{id}成功")
    else:
        message.reply(f"设置失败！请查看模型列表。当前出包王女模型为{jpspeaker_id}号")

def getmodellist(commandData,message: Message):
    message.reply(f"中文模型{idmessage_cn}\n日文模型{idmessage_jp}\n出包王女模型{idmessage_tolove}")

def getultramodellist(commandData,message: Message):
    replylist = ''
    for i, info in models_info.items():
        if not info['enable']:
            continue
        replylist = f"{replylist}角色名：{info['name_zh']},语言：{info['language']},Type:{info['type']}\n"
    message.reply(f"额外模型列表如下：\n{replylist}")

def getnewssend(commandData,message: Message):
    getnews(max_behot_time, title, source_url, s_url, source, media_url)
    now = zhihu.get_time()
    replytexts = f'{now}今日新闻\n'
    for i in range(len(title)):
        if int(i) > 7 :
            break
        replytexts = f"{replytexts}{title[i]}\n{s_url[i]}\n"
    message.reply(replytexts.encode('GBK','ignore').decode('GBk') )

def getzhihuhot(commandData,message: Message):
    rows = zhihu.save_hot_list()
    now = zhihu.get_time()
    replytexts = f"{now}今日知乎热榜\n"
    for i in range(len(rows)):
        if int(i) > 7:
            break
        replytexts = f"{replytexts}热榜{rows[i][r'排名']}:{rows[i][r'标题']};热度:{rows[i][r'热度(万)']}\n{rows[i]['问题链接']}\n"
    message.reply(replytexts.encode('GBK','ignore').decode('GBk') )

def bbspeech(commandData,message: Message):
    texts = commandData[0]
    generateSound(f"[ZH]{texts}[ZH]",0,0,2)
    with open("output.wav", "rb") as audio_file:
        # 读取内容并编码为Base64格式
        audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
    cqapi.send_group_msg(message.group_id, record('base64://' + audio_base64))


bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        # 366379083 # 替换为你的QQ群号
    ],
)
bot.on_group_msg = on_group_msg
# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo - 输出文本"
    ],
    "type": "all"
}).command(chat, "chatglm", {
    # echo 帮助
    "help": [
        "#chatglm - 进行chatglm对话"
    ],
    "type": "group"
}).command(reset, "重置", {
    # echo 帮助
    "help": [
        "#重置 - 清空chatglm的历史记录"
    ],
    "type": "group"
}).command(neko, "变猫娘", {
    # echo 帮助
    "help": [
        "#变猫娘 - 使chatglm变成猫娘"
    ],
    "type": "group"
}).command(startchatglm, "启动chatglm", {
    # echo 帮助
    "help": [
        "#启动chatglm - 启动chatglm服务"
    ],
    "type": "group"
}).command(speakzh, "中文说", {
    # echo 帮助
    "help": [
        "#中文说 - 文字转中文语音"
    ],
    "type": "group"
}).command(speakjp, "日文说", {
    # echo 帮助
    "help": [
        "#日文说 - 文字转日文语音"
    ],
    "type": "group"
}).command(setchatglm_speak, "chat设置", {
    # echo 帮助
    "help": [
        "#chat设置 - 启动格式：{start} + {设置语言[eg:zh or jp]} + {说话人[num]} "
    ],
    "type": "group"
}).command(setzhspeakid, "中文模型设置", {
    # echo 帮助
    "help": [
        "#中文模型设置 - num : 直接输入模型编号"
    ],
    "type": "group"
}).command(setjpspeakid, "日文模型设置", {
    # echo 帮助
    "help": [
        "#日文模型设置 - num : 直接输入模型编号"
    ],
    "type": "group"
}).command(getmodellist, "模型列表", {
    # echo 帮助
    "help": [
        "#模型列表 - 列出模型列表"
    ],
    "type": "group"
}).command(speaktolove, "出包说", {
    # echo 帮助
    "help": [
        "#出包说 - 出包王女语音输出"
    ],
    "type": "group"
}).command(settolovespeakid, "出包模型设置", {
    # echo 帮助
    "help": [
        "#出包模型设置 - num : 直接输入模型编号"
    ],
    "type": "group"
}).command(getultramodellist, "额外模型列表", {
    # echo 帮助
    "help": [
        "#额外模型列表 - echo list(查看角色名后无需指令码紧跟说或say使用）"
    ],
    "type": "group"
}).command(getnewssend, "今日新闻", {
    # echo 帮助
    "help": [
        "#今日新闻 - echo 今日头条新闻"
    ],
    "type": "group"
}).command(getzhihuhot, "知乎热榜", {
    # echo 帮助
    "help": [
        "#知乎热榜 - echo 今日知乎热榜"
    ],
    "type": "group"
})
#     .command(bbspeech, "朗读", {
#     # echo 帮助
#     "help": [
#         "#朗读 - 标贝女声音库朗读"
#     ],
#     "type": "group"
# })




bot.start()