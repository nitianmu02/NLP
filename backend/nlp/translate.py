# used for test demo

import requests
import hashlib
url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
appid = "20230424001654753"
salt = '42'
key = 'egbame2d6QRlW362pFjQ'
def translate(text, target_lang):
    
    md5 = hashlib.md5()
    sign = appid + text + salt + key
    sign = sign.encode('utf-8')
    md5.update(sign)
    sign = md5.hexdigest()

    params = {
        "q": text,
        "from": "auto",
        "to": target_lang,
        "appid": appid,
        "salt": salt,
        "sign": sign
    }

    response = requests.get(url, params=params)

    result = response.json()
    if "trans_result" in result.keys():
        return result["trans_result"][0]["dst"]
    else:
        return ''
