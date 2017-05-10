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
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text=str(event.message)))

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
'''
	line_bot_api.reply_message(
		event.reply_token,
		StickerSendMessage(
			package_id=event.message.package_id,
			sticker_id=event.message.sticker_id)
	)
'''
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(text="HA! HA! So funny"))
#url_for('v_contacts',_external=True)
'''
@app.route("/")
def index():
	return "<p>Hello World!</p>"
'''
if __name__ == "__main__":
	app.run()