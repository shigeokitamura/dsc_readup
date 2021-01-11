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


#VoiceText Web API
API_KEY = df["voicetext"]
url = "https://api.voicetext.jp/v1/tts"

async def fetch(session, url, data_fm):
    with async_timeout.timeout(10):
        async with session.post(url, auth=aiohttp.BasicAuth("a8o3kaexy5vj1hv9", ""), data=data_fm) as response:

            if response.status != 200 :
                print("Error API : " + str(response.status))
                print(await response.json())

            return await response.read()

async def knockApi(makemsg, msger, speed, r_range, pitch, group):

    #バイナリデータの一時保存場所
    tmp = "./cache/{}/".format(group)

    if not os.path.isdir(tmp):
        os.makedirs(tmp)

    # voicetext パラメーター設定
    # ===========================================

    """
    参考）https://cloud.voicetext.jp/webapi/docs/api

        "speaker": "show", "haruka", "hikari", "takeru", "santa", "bear"
        "speed": 話す速度。基準値:100(%)、範囲:50~400
        "pitch": 声の高さ。基準値:100(%)、範囲:50~200
        "text": 本文。
    """

    # パラメーター調整
    try:
        speaker_id = int(msger)
        if speaker_id < 1 or speaker_id > 6:
            speaker_id = 1
    except:
        speaker_id = 1

    if speed < 0.5 or speed > 4.0:
        speed = 1.0

    if pitch < 0.5 or pitch > 2.0:
        pitch = 1.0

    speaker = [None, "show", "haruka", "hikari", "takeru", "santa", "bear"]

    prm = {
        "speaker": speaker[speaker_id],
        "speed": int(speed * 100),
        "pitch": int(pitch * 100),
        "text": makemsg[:120] # APIの文字数制限
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

    # VoiceText APIアクセス
    # ===========================================
    print("Start API")
    print(prm)
    async with aiohttp.ClientSession() as session:
        response = await fetch(session,
            url,
            data_fm=prm
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
