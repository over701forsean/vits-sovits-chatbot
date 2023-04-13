# vits-sovits-chatbot

## 项目介绍
  >结合chatglm，vits，vits，pycqBot的本地部署qq聊天机器人。<br>
  让喜欢的日语系角色(so-vits模型)说中文，唱歌，并且在qq上以语音形式发出。除此之外还搭载了中日文近50名角色(vits模型)。<br>
  一个自动chatglm回复你并且可以附带不同语言的语音的对话机器人。<br>
  使用了几个非常好的项目 [chatglm-6B](https://github.com/THUDM/ChatGLM-6B)，[ChatWaifu](https://github.com/cjyaddone/ChatWaifu)，[pycqBot](https://github.com/FengLiuFeseliud/pycqBot) ,[so-vits-svc](https://github.com/svc-develop-team/so-vits-svc),[vits-mandarin-windows](https://github.com/rotten-work/vits-mandarin-windows)结合在一起，在其之上添加我所需的功能。我会写出我在编写过程中遇到的一些重要的问题，供大家参考，在代码上的不规范请多多包涵。<br>
  
## 功能
  >一个qq机器人，监听消息。<br>
  一个标贝标准中文女声tts，用于朗读。基于[vits-mandarin-windows](https://github.com/rotten-work/vits-mandarin-windows)(指令为#朗读)<br>
  为了解决日语系角色说中文tts效果不好、训练集太少、训练集带有口癖等问题导致的tts模型较差，但是又想让日语系角色说中文的问题。从标准中文女生tts出发，经日语系角色sovits模型可使日语系角色说出流利的中文。<br>
  sovits模型随机唱歌，并以语音形式发送qq消息。(从raw中的干声文件随机挑选一首)<br>
  chatglm模型加载进行智能对话，可自定义历史（已预设猫娘）。(你也可以将chatgptapi接入，请参考其他项目比如[PyChatGPT](https://github.com/rawandahmad698/PyChatGPT)<br>
  回复语音（base64编码）（中/日）。包括chatglm对话（选择开启）,总共近50个模型。对于额外模型不计入指令，请查看额外模型列表中角色中文名并直接发送{name}讲/说{content}。<br>
  获取今日新闻和知乎热榜。<br>
  可前往[vits-sovits-chatbot 简单演示效果](https://www.bilibili.com/video/BV1CV4y1X7qq)看简单演示。<br>
  具体功能请具体运行机器人后#help查看帮助，或是查看pycq.py文件。
  
## 项目安装
  可参考[vits-sovits-chatbot 简洁安装演示](https://www.bilibili.com/video/BV1bc411L72n)简洁安装演示。<br>
  <br>
  #WARNING:pycqBot项目更新，import类时有所变化，请参考pycqBot文档将其相关import语句变动。若遇到cqhttp提示的版本问题，请更新cqhttp的exe文件。若配置的版本对不上，请在空白文件夹处单独存放cqhttp的exe并用pycqBot初始化出配置文件后再覆盖到本项目中使用，<br>
  <br>
  下载最新的[release](https://github.com/over701forsean/vits-sovits-chatbot/releases),解压到某个目录下。<br>
  <br>
  >模型下载：<br>
  从[ChatWaifu](https://github.com/cjyaddone/ChatWaifu)中下载模型，其应为柚子社角色，置于model文件夹中。<br>
  从[TTSModels](https://github.com/CjangCjengh/TTSModels)中下载To Love模型与config，置于名为ToLove文件夹中，并将该文件夹置于model文件夹中。<br>
  从[vits-mandarin-windows](https://github.com/rotten-work/vits-mandarin-windows),找到标贝中文标准女声音库预训练权重，并下载，置于model文件夹中。<br>
  下载额外的[vits-model](https://huggingface.co/spaces/sayashi/vits-models/tree/main/pretrained_models)。并将其放入pretrained_models文件夹中，不要覆盖info.json<br>
  参见[so-vits-svc](https://github.com/svc-develop-team/so-vits-svc),其中有预先下载的模型文件checkpoint_best_legacy_500.pt,按指示放入hubert文件夹中。<br>
  请把你的sovits模型(G开头)与config文件放入logs\44k中，并打开config文件，查看最底下'spk'的值，打开本项目中inference_main.py文件，将waifuname = 'riri'中的riri改为你的'spk'的值。除此以外，请查看#一定要设置的部分的前两项，更改为你的sovits的模型和config名称。如果需要唱歌，请放入干声wav后将名称集合替换第四项。<br>
  <br>
  
  >参数调整：<br>
  打开本项目中config.yml文件，填写你的机器人qq号与密码。<br>
  打开本项目中pycq.py文件，找到if message.user_id == 000000000:，将一串0改为你的主qq号。<br>
  <br>
  
  >环境搭建：<br>
  运行Anaconda Promt，使用conda create -n <环境名称> python=3.9，新建一个虚拟环境。<br>
  继续执行conda activate <环境名称>,切换到刚才创建的虚拟环境。<br>
  移动到本项目目录下(使用cd),执行pip install -r requirements.txt,安装依赖项。<br>
  <br>
  
  >项目运行：<br>
  在虚拟环境中在本项目目录下，python pycq.py，登录机器人qq，登陆成功后即运行成功。<br>
  或是从IDE中（比如pycharm）打开，选择该虚拟环境，运行pycq.py。<br>
  <br>
  


  >从零开始（不推荐）依照我配置的顺序说明步骤：<br>
  1.下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp),这是通信的核心。<br>
  2.安装[pycqBot](https://github.com/FengLiuFeseliud/pycqBot),并按照文档初运行，成功登陆你的账号。<br>
  3.安装[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)，执行其demo，确保你可以运行。<br>
  4.安装[ChatWaifu](https://github.com/cjyaddone/ChatWaifu)，项目已经集成了vits且自带模型，十分便利，确保能听到对的声音。<br>
  5.下载额外的[vits-model](https://huggingface.co/spaces/sayashi/vits-models/tree/main/pretrained_models)。<br>
  6.下载标贝中文女声模型[vits-mandarin-windows](https://github.com/rotten-work/vits-mandarin-windows)。<br>
  7.下载[so-vits-svc](https://github.com/svc-develop-team/so-vits-svc),并将其整合到你的主项目中。<br>
  5.请参考我的代码修改。（由于魔改的文件太多，本人已经记不全所有魔改过的地方了）<br>
  6.运行pycq.py文件。<br>
  
## 拓展模型
  >vits的音频生成函数在ChatWaifu.py的GenerateSound函数里。其中正常的config下的模型按whichmodel==0参考改写。单config关联多模型的按whichmodel==1参考改写。像标贝女声那个项目一样config缺斤少两的，自己研究config里面需要传递的参数，比如symbols和cleaners都不同，这些自行摸索。svc的模型基本跟原项目相同，直接在生成音频文件处改参数设置就行。
 
## 一些感想
  >在pycqBot中函数已经封装的很好了，但我在尝试发送语音时总是遇到看不到语音的情况。一些CQCode发送时不能包含其它信息，而pycqBot项目中使用reply()会自动在传入cqhttp的api前包含对消息的回复（这一信息），所以只能直接使用cqapi的函数发送此类CQCode。<br>
  在选择tts模型时一开始让我十分崩溃，由于我最初想要说话的角色的训练数据十分少（只有完整的一段ASMR）且不适合训练（气声多且为日文），本着先选好模型再sovits转角色的想法去huggingface找模型。中文模型只有一个facebook数据训练的基于fairseq框架的模型，然而他的示例使用代码执行到sample的时候会到sklearn-crfsuite模块中出现了使用ascii编码的错误，而错误的地方在一个pyd文件中而不得不放弃更改。几经辗转才去使用vits。直接从vits项目出发搭建可能是较为麻烦的，而ChatWaifu这样的封装项目会省去一些功夫。

## 注意事项
  >ChatWaifu中我已将语音生成打包为函数，并将其wav数据作为返回值，但并未使用，暂不清楚使用该wav数据直接转base64数据能否上传，可自行尝试。<br>
  CQCode格式请参考go-cqhttp的文档，也有大佬指点说可以去看NoneBot的源码更进一步。<br>
  qq机器人指令参考pycqBot的文档，除了单独类型的CQCode都可以仿照编写。<br>
  模型的添加删除与索引请查看ChatWaifu。
  
  
  

