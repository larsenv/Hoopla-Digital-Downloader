# Hoopla Digital Downloader

This'll let you download from Hoopla Digital.

You need a Widevine CDM L3 in pywidevine/L3/cdm/devices/android_generic/ in order to use it.

Can also grab keys even if content's removed from Hoopla.
Most content on Hoopla is limited to 480p.

You will have to install the requirements by running `pip install -r requirements.txt`, then you can run hoopla-key.py by running `python hoopla-key.py <url> <token>`.

## Instructions to grab your Hoopla Digital token

1. Borrow an item on Hoopla.")
2. Play the content and immediately open developer mode before the content loads."
3. Grab the value of the dt-custom-data request header on the POST request to https://lic.drmtoday.com/license-proxy-widevine/cenc/.