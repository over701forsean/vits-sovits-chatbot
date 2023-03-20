# chatglm-vits-pycqbot-chatbot

## 项目介绍
  结合chatglm，vits，cqhttp的本地部署qq聊天机器人。<br>
  一个自动chatglm回复你并且可以附带不同语言的语音的对话机器人，所以抛开chatglm进行说话也是可以的。<br>
  使用了几个非常好的项目 [chatglm-6B](https://github.com/THUDM/ChatGLM-6B)，[ChatWaifu](https://github.com/cjyaddone/ChatWaifu)，[pycqBot](https://github.com/FengLiuFeseliud/pycqBot) 结合在一起，在其之上添加我所需的功能。我会写出我在编写过程中遇到的一些重要的问题，供大家参考，在代码上的不规范请多多包涵。
  
## 功能
  chatglm模型加载进行智能对话。<br>
  回复语音（base64编码）（中/日）。包括chatglm对话（选择开启）<br>
  更多功能待开发···（先歇会）
  
## 项目环境
  下面依照我配置的顺序说明步骤：<br>
  1.下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp),这是通信的核心。<br>
  2.安装[pycqBot](https://github.com/FengLiuFeseliud/pycqBot）,并按照文档初运行，成功登陆你的账号。<br>
  3.安装[ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)，执行其demo，确保你可以运行。<br>
  4.安装[ChatWaifu](https://github.com/cjyaddone/ChatWaifu)，项目已经集成了vits且自带模型，十分便利，确保能听到对的声音。<br>
  5.将本项目文件copy进文件夹中并替换，或者你可以参考我的代码自行编写。<br>
  6.运行pycq.py文件。<br>
  ___
  另辟蹊径(不推荐，需要确保模块)：<br>
  下载release里的文件，直接运行pycq。<br>
  
## 一些感想
  在pycqBot中函数已经封装的很好了，但我在尝试发送语音时总是遇到看不到语音的情况。一些CQCode发送时不能包含其它信息，而pycqBot项目中使用reply()会自动在传入cqhttp的api前包含对消息的回复（这一信息），所以只能直接使用cqapi的函数发送此类CQCode。<br>
  在选择tts模型时一开始让我十分崩溃，由于我最初想要说话的角色的训练数据十分少（只有完整的一段ASMR）且不适合训练（气声多且为日文），本着先选好模型再sovits转角色的想法去huggingface找模型。中文模型只有一个facebook数据训练的基于fairseq框架的模型，然而他的示例使用代码执行到sample的时候会到sklearn-crfsuite模块中出现了使用ascii编码的错误，而错误的地方在一个pyd文件中而不得不放弃更改。几经辗转才去使用vits。直接从vits项目出发搭建可能是较为麻烦的，而ChatWaifu这样的封装项目会省去一些功夫。

## 注意事项
  ChatWaifu中我已将语音生成打包为函数，并将其wav数据作为返回值，但并未使用，暂不清楚使用该wav数据直接转base64数据能否上传，可自行尝试。
  CQCode格式请参考go-cqhttp的文档，也有大佬指点说可以去看NoneBot的源码更进一步。
  qq机器人指令参考pycqBot的文档，除了单独类型的CQCode都可以仿照编写。
  模型的添加删除与索引请查看ChatWaifu。
  
  
  

