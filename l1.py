# -*- coding: utf-8 -*-
# Module: KEYS-L1
# Created on: 11-10-2021
# Authors: -∞WKS∞-
# Version: 1.1.0

import base64, requests, sys, xmltodict
import headers
from pywidevine.L1.cdm import cdm, deviceconfig
from base64 import b64encode
from pywidevine.L1.getPSSH import get_pssh
from pywidevine.L1.decrypt.wvdecryptcustom import WvDecrypt

pssh = input('\nPSSH: ')
lic_url = input('License URL: ')

def WV_Function(pssh, lic_url, cert_b64=None):
    wvdecrypt = WvDecrypt(init_data_b64=pssh, cert_data_b64=cert_b64, device=deviceconfig.device_android_generic)                   
    widevine_license = requests.post(url=lic_url, data=wvdecrypt.get_challenge(), headers=headers.headers)
    license_b64 = b64encode(widevine_license.content)
    wvdecrypt.update_license(license_b64)
    Correct, keyswvdecrypt = wvdecrypt.start_process()
    if Correct:
        return Correct, keyswvdecrypt   
correct, keys = WV_Function(pssh, lic_url)

print()
for key in keys:
    print('--key ' + key)
