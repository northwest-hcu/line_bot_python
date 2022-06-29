import os,sys,json,pprint
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import openWeather as ow

#flask
app = Flask(__name__)

fp=open('./secret.json','r',encoding='utf-8')
data=json.load(fp)

#鍵の定義
channel_secret=data['channel_secret']
channel_access_token=data['channel_access_token']
if channel_secret is None:
    print('秘密鍵が存在しません.')
    sys.exit(1)
if channel_access_token is None:
    print('チャンネルへのアクセストークンが存在しません.')
    sys.exit(1)

#LINEbot関係のインスタンス
line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

#example.com/callbackをwebhook URLに設定してる場合
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    """
    print('events:')
    [print(i) for i in events]
    print('body:'+body)
    """

    #print('User ID:'+events.source.userId)
    #pprint.pprint(json.loads(body),width=40)
    events=events[0]

    if events.message.type=="image":
        print('画像を受信しました.')
        line_bot_api.reply_message(
            events.reply_token,
            TextSendMessage(text='画像を受け取りました.')
        )
    elif events.message.type=="text":
        # print('テキスト< '+events.message.text+' >を受信しました.')
        ans = ow.getWeatherInfo(events.message.text)
        line_bot_api.reply_message(
            events.reply_token,
            #TextSendMessage(text='テキストを受け取りました.')
            TextSendMessage(text=ans)
        )

    # if event is MessageEvent
    """
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text+'//')
        )
    """

    return 'OK'

#このファイルがインポートされたものでなければ実行する
if __name__=="__main__":
    app.run(port=8080,host='localhost')
