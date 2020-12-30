喋太郎
====

Overview
これは、DiscordのTTS Botです。

## Description
テキストチャンネルに入力されたテキストを元に合成音声APIを用いて音声ファイルを生成し、ボイスチャンネルで再生するBotです。

## Demo
https://www.nicovideo.jp/watch/sm34363918

ただし、この動画の喋太郎はバージョンが古いです。


## VS.
Discordアプリケーションに組み込みであるTTS機能と違い、ボイスチャンネルに呼び出しておけば、居る間は自動で読み上げてくれます。また、辞書登録機能もあるので、読み間違いも是正していくことができます。

## Requirement
- python3.6.5
- discord.py 1.0.0a
- opus
- libffi
- ffmpeg --with-opus
- postgresql

その他、必要なライブラリは `requrire.txt` に記述してあります。
それとは別に、以下のものが必要になります。
- Discord Bot Token
- docomo Developer support API key
    - 音声合成【Powerd by NTTテクノクロス】の利用申請を行なっているもの

## Usage
招待URLから、管理しているサーバへ招待してください。
その後の使い方は、以下の記事に書いてあります。　　
https://www.dayaman.work/syabetaro/info

## Install
まず、Requirementにあるパッケージをインストールしてください。次に、
```
$ pip install -r requirements.txt
```
で必要なライブラリをインストールしてください。
次に、postgresqlでデータベースを作成しておきます。
次に、`token.json.example`を`token.json`にリネームします。内容を以下で指定したように適宜書き換えてください。
```
"docomo":"docomo Deveroper TOKEN",
"bot":"BOT TOKEN",
"manager_id":"BOT MANAGER DISCORD ID", #Bot管理人のDiscord ID
"db_user":"taro", # データベースのユーザ
"db_name":"taro_dsc" # データベースの名前
```
設定が終わったら、
```
$ python ctrl_db.py
```
を実行して、テーブルを作成します。
そのあとは、
```
$ python main.py
```
でBotが起動します。

## LICENSE
This software is released under the MIT License, see LICENSE.txt.
