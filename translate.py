import requests
import random
import hashlib
import time

def salt_sign(e):
   navigator_appVersion = "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
   t = hashlib.md5(navigator_appVersion.encode("utf-8")).hexdigest()
   r = str(int(time.time() * 1000))
   i = r + str(random.randint(1, 10))
   return {
       "ts": r,
       "bv": t,
       "salt": i,
       "sign": hashlib.md5(str("fanyideskweb" + e + i + "Ygy_4c=r#e#4EX^NUGUc5").encode("utf-8")).hexdigest()
  }

def translate(word):
   url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
   r = salt_sign(word)
   data = {
       "i": word,
       "from": "AUTO",
       "to": "ja",
       "smartresult": "dict",
       "client": "fanyideskweb",
       "salt": r["salt"],
       "sign": r["sign"],
       "lts": r["ts"],
       "bv": r["bv"],
       "doctype": "json",
       "version": "2.1",
       "keyfrom": "fanyi.web",
       "action": "FY_BY_REALTlME"
  }
   headers = {
       "Cookie": "OUTFOX_SEARCH_USER_ID=-286220249@10.108.160.17;",
       "Referer": "http://fanyi.youdao.com/",
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
  }
   res = requests.post(url=url, data=data, headers=headers).json()
   return res['translateResult'][0][0]['tgt']

def translatezhja(word:str):
    try:
        jaword = translate(word)
        return jaword
    except Exception as e:
        return e


if __name__ == '__main__':
   while True:
       try:
           worded = input("请输入你要翻译的单词或短句:")
           print(translatezhja(worded))
       except Exception as e:
           print("错误:", e)