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

from msg_classifier_lg import msg_predict

app = Flask(__name__)

#line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
#handler = WebhookHandler('YOUR_CHANNEL_SECRET')
line_bot_api = LineBotApi('2mxE4Ky4O15Ss5qR9EzfCeFmbKYrm1vdUmNMoeJgzW/vDW6GNowXAtSVJ8AUQsR+Ru3VaOdSIkQfLWXMDcDi4rhrwDfQ5p1eJepEDXq+Z+GwmoOej5ZsmqvhXA/mXJ2zzunzm+VcF9Ws7zoT+oyzXAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('38a504945e12d5a6bd5902af2ac3a4cf')

switch = []

class_dic = {0:"chat", 1:"objective information", 2:"subjective information"}

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

	if event.message.text == "詐騙奧特關閉".decode("utf-8") and event.Source.UserID not in switch:
		switch.append(event.Source.UserID)
		print("add", event.Source.UserID)
		line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="詐騙奧特已關閉，請輸入「詐騙奧特開啟」啟動服務"))

	elif event.message.text == "詐騙奧特開啟".decode("utf-8") and event.Source.UserID in switch:
		switch.remove(event.Source.UserID)
		print("remove", event.Source.UserID)
		line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="詐騙奧特已啟動"))

	elif event.message.id not in switch:
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(text=class_dic[msg_predict(event.message.text)]))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="HA! HA! So funny"))

if __name__ == "__main__":
	app.run()