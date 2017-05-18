# -*- coding: utf8 -*-

from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, StickerMessage
)
#import msg_classifier_lg
from msg_classifier_lg import msg_predict
'''
import jieba
import jieba.analyse
from sklearn.externals import joblib
# jieba setup
jieba.set_dictionary("./archive/dict.txt.big")
jieba.analyse.set_stop_words("./archive/stop_words.txt")
clf = joblib.load('./archive/classifier_lg_model.pkl')
'''
app = Flask(__name__)

#line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
#handler = WebhookHandler('YOUR_CHANNEL_SECRET')
line_bot_api = LineBotApi('2mxE4Ky4O15Ss5qR9EzfCeFmbKYrm1vdUmNMoeJgzW/vDW6GNowXAtSVJ8AUQsR+Ru3VaOdSIkQfLWXMDcDi4rhrwDfQ5p1eJepEDXq+Z+GwmoOej5ZsmqvhXA/mXJ2zzunzm+VcF9Ws7zoT+oyzXAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('38a504945e12d5a6bd5902af2ac3a4cf')

@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']
	print("signature: ", signature)
	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)
	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		abort(400)

	return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
	result = msg_predict(str(event.message.text))
	if result == 0:
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text="chat"))
		return 'OK'
	elif result == 1:
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text="objective information"))
		return 'OK'
	elif result == 2:
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text="subjective information"))
		return 'OK'
	return 'OK'

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="HA! HA! So funny"))
	
	line_bot_api.reply_message(
		event.reply_token,
		StickerSendMessage(
			package_id=event.message.package_id,
			sticker_id=event.message.sticker_id)
	)

if __name__ == "__main__":
	app.run()