from flask import Flask, request, abort, send_file
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import(
    Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage,
    StickerMessage, FlexMessage, FlexContainer
)
from linebot.v3.webhooks import(
    MessageEvent, TextMessageContent, LocationMessageContent, StickerMessageContent
)
import os
import configparser

from richmenu import set_menu
from quickreply import handle_text_message, operation_instruction,get_quick_reply_text
from flexmessage import get_restaurant_info, flex_message
import logging



app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# read channel assess token and channel secert
config = configparser.ConfigParser()
config.read('config.ini')
configuration = Configuration(access_token=config.get('line-bot','channel_access_token'))
handler = WebhookHandler(config.get('line-bot','channel_secret'))
richmenu_id = config.get('line-bot','richmenu_id')

# set header for http request
HEADER = {
    'Content-type' : 'application/json',
    'Authorization' : F'Bearer {config.get("line-bot", "channel_access_token")}'
}

@app.route("/callback", methods=["POST","GET"])
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

# import richmenu from richmenu.py and set
def set_rich_menu():
    image_path = set_menu()
    return send_file(image_path, mimetype='image/png')

user_session = {}
# user click richmenu then send response
# call quickreply.py function
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_id = event.source.user_id
        text = event.message.text
    
        if text == "操作說明":
            response_message = operation_instruction()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=response_message)]))
            
        elif get_quick_reply_text(text):
            user_session[user_id] = {'restaurant_type': text}
            handle_text_message(event)


# when user send location then send the recommand information
@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        user_id = event.source.user_id
        user_data = user_session.get(user_id, {})
        restaurant_type = user_data.get('restaurant_type')
        user_latitude = event.message.latitude
        user_longitude = event.message.longitude
        radius_km = 10

        restaurant_info = get_restaurant_info(restaurant_type, user_longitude, user_latitude,radius_km)

        if not restaurant_info:
            reply_text = TextMessage(text= "附近無推薦餐廳🤐")
            line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[reply_text]))
            
        else:
            flex_content = flex_message(restaurant_info)
            reply_flex = FlexMessage(altText="Info", contents=FlexContainer.from_dict(flex_content))
            line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[reply_flex]))

# user send sticker then response sticker
@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    StickerMessage(package_id="8522", sticker_id="16581277"),
                ]
            )
        )



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    app.run(host="0.0.0.0", port=port, debug=True)



