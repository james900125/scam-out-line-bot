# -*- encoding: utf-8 -*-

from flask import Flask, request, abort

import os
import sys

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage, TextSendMessage, StickerSendMessage, StickerMessage, 
	SourceUser, SourceGroup, SourceRoom
)

from msg_response import Msg_response

#### Data Prepare ###
msg = Msg_response()
msg.setup()
msg.data_prepare()

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.environ.get('LINE_CHANNEL_SECRET', None)
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
    
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


switch = []

#class_dic = {0:"chat", 1:"objective information", 2:"subjective information"}

@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

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

	if isinstance(event.source, SourceGroup):  #define MessageEvent from group/room/user
		reply_id = event.source.group_id
		type_id = "group"
	elif isinstance(event.source, SourceRoom):
		reply_id = event.source.room_id
		type_id = "room"
	else:
		reply_id = event.source.user_id
		type_id = "user"

############## Turn on/off service operation #############

	if event.message.text == "詐騙奧特關閉".decode("utf-8") and reply_id not in switch:
		switch.append(reply_id)
		print "add ID: {} in switch, the ID is {} type.".format(reply_id, type_id)
		line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="詐騙奧特已關閉，請輸入「詐騙奧特開啟」啟動服務"))

	elif event.message.text == "詐騙奧特開啟".decode("utf-8") and reply_id in switch:
		switch.remove(reply_id)
		print "remove ID: {} from switch, the ID is {} type.".format(reply_id, type_id)
		line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="詐騙奧特服務已啟動"))

#############################################################

	elif reply_id not in switch:
		if msg.msg_predict(event.message.text) != 1: return 0   #define message 0:chat / 1:objective / 2:subjective
		result, score = msg.compare(event.message.text)   #searching message is in gov_api or not 
		print "the message compared result:{} , score:{}".format(result, score)
		if score > 20:   #message is in gov_api
			line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text=u'此文章為捏造的謠言!\n政府已有發出澄清文:\n' + msg.gov_data[result]))
			return 0

		#message is not in gov_api, 檢查可疑訊息資料庫
		msg.data_prepare_suspect()      
		result_suspect, score_suspect = msg.compare_suspect(event.message.text)
		if len(msg.suspect_data) != 0 and score_suspect > 20: #若已收錄該則可疑訊息，更新 db 的 count 欄位
			msg.update_suspect(result_suspect) 
		else:
			msg.insert_suspect(event.message.text) #若還沒收錄，則新增一筆資料至db

		#message is not in gov_api 的統一回覆
		line_bot_api.reply_message(
				event.reply_token,
				TextSendMessage(text="此文章有潛在謠言嫌疑，請進行查證，避免上當受騙"))

if __name__ == "__main__":
	app.run()