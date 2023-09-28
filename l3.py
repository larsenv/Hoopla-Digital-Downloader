# -*- coding: utf-8 -*-
# Module: KEYS-L3
# Created on: 11-10-2021
# Authors: -∞WKS∞-
# Version: 1.1.0

# Modified by: CrymanChen
# Modified on: April 7, 2023

import base64, requests, sys, xmltodict
import headers

# 增加了一个第三方库pyperclip, 目的是将key(有时是多个key)快速复制到剪贴板中
import pyperclip
from pywidevine.L3.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L3.getPSSH import get_pssh
from pywidevine.L3.decrypt.wvdecryptcustom import WvDecrypt

pssh = sys.argv[1]
lic_url = sys.argv[2]


def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(
        init_data_b64=pssh,
        cert_data_b64=cert_b64,
        device=deviceconfig.device_android_generic,
    )
    widevine_license = requests.post(
        url=lic_url, data=wvdecrypt.get_challenge(), headers=headers.headers
    )
    # 说明:
    # 第24行需要根据不同的License类型做出调整, 不是一成不变的, 举例如下:
    # ①查看License请求的cURL, 转换成适配Python的语句, 若最后一行像下面这样:
    # response = requests.post('这里是License URL', headers=headers, data=data,)
    # 则第24行无需修改, 只需将headers复制到headers.py中, 注意消息体的类型(Content-Type)有时不是application/x-www-form-urlencoded
    # ②若最后一行像下面这样:
    # response = requests.post('这里是License URL', headers=headers, data=data, params=params)
    # 则需要增加参数(params), 一般解决办法是在"headers=headers.headers"的后面加入", json=params", 让参数以json格式传出去, 否则通常会返回HTTP 400/403/502
    license_b64 = b64encode(widevine_license.content)
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    if Correct:
        return Correct, keyswvdecrypt


correct, keys = WV_Function(pssh, lic_url)

print()
for key in keys:
    print("--key " + key)

# 建立key_string字符串, 使得所有key进行如下变换: ①添加前缀"--key" ②使得每一个带有前缀的key以空格的形式连接起来(方便multi-keys时一键复制)
key_string = " ".join([f"--key {key}" for key in keys])
# 使用导入的pyperclip库, 将key_string字符串复制至剪贴板, 省去手动选择"--key {key}"、复制、粘贴的麻烦
pyperclip.copy(key_string)
