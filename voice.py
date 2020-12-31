# ソースはこちらから引用・改修 http://blog.cgfm.jp/garyu/archives/3396
import json
import os
import sys
import datetime
import argparse
import subprocess
import requests
import aiohttp
import asyncio
import async_timeout
import pprint


# config
# ===========================================
with open('token.json') as f:
    df = json.load(f)


#Docomo 音声合成 API
API_KEY = df['docomo']
url = "https://api.apigw.smt.docomo.ne.jp/futureVoiceCrayon/v1/textToSpeech?APIKEY="+API_KEY

async def fetch(session, url, data_fm, headers):
    with async_timeout.timeout(10):
        async with session.post(url, data=data_fm, headers=headers) as response:

            if response.status != 200 :
                print("Error API : " + str(response.status))
                exit()

            return await response.read()

async def knockApi(makemsg, msger, speed, r_range, pitch, group):

    #バイナリデータの一時保存場所
    tmp = "./cache/{}/".format(group)

    if not os.path.isdir(tmp):
        os.makedirs(tmp)

    # aitalk パラメーター設定
    # ===========================================

    """
    参考）音声合成 | docomo Developer support
    https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=text_to_speech&p_name=api_7#tag01

        'speaker' : "nozomi"、"seiji"、"akari"、"anzu"、"hiroshi"、"kaho"、"koutarou"、"maki"、"nanako"、"osamu"、"sumire"
        'pitch' : ベースライン・ピッチ。 基準値:1.0、範囲:0.50～2.00
        'range' : ピッチ・レンジ。基準値:1.0、範囲:0.00～2.00
        'rate' : 読み上げる速度。基準値:1.0、範囲:0.50～4.00
        'volume' : 音量。基準値:1.0、範囲:0.00～2.00
    """

    prm = {
        "Command": "AP_Synth",
        "SpeakerID": msger,
        "StyleID": msger,
        "SpeechRate": speed,
        "VoiceType": r_range,
        "AudioFileFormat": 2,
        "TextData": makemsg
    }
    # パラメーター受取
    # ===========================================
    #%% arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--text',      type=str,   required=True)
    args = parser.parse_args()
    text = args.text
    """

    # Docomo APIアクセス
    # ===========================================
    print("Start API")
    print(prm)
    async with aiohttp.ClientSession() as session:
        response = await fetch(session,
            url,
            data_fm=json.dumps(prm),
            headers={
                'Content-Type': 'application/json',
                'Accept' : 'audio/L16'
            }
        )

    #現在日時を取得
    now = datetime.datetime.now()
    tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S%f')

    #保存するファイル名
    rawFile = tstr + ".wav"

    #バイナリデータを保存
    fp = open(tmp + rawFile, 'wb')
    fp.write(response)
    fp.close()

    # PCM名を返す
    return rawFile
