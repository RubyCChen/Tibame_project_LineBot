from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    LocationAction,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    ReplyMessageRequest,
)
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
configuration = Configuration(access_token=config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret')) 
api_client = ApiClient(configuration=configuration)
messaging_api = MessagingApi(api_client=api_client)

# operation instruction text
def operation_instruction():
    return """🔥 現在就開始！使用LINE尋找你的下一餐！快速行動！ 🔥

步驟 1: 🍔 快速選擇你的食物: 立即做出選擇！你的選項包括漢堡、義大利麵、拉麵、壽司和排骨飯。不許猶豫，選一個！

步驟 2: 📍 立刻分享你的位置: 選定食物後，LINE會要求你分享位置。不要拖拉，使用LINE的位置分享功能，現在就做！

步驟 3: 🍽️ 準備接收餐廳推薦: 位置一旦分享，就坐等LINE推薦餐廳。這將是你的用餐指令，做好準備！

⚠️ 這些步驟要快速完成，不許拖泥帶水。你的任務就是高效率地選擇和用餐！ ⚠️ """

# when user click richmenu will return text
def get_quick_reply_text(user_text):
    get_text = ["拉麵", "壽司", "漢堡", "義大利麵", "排骨飯", "操作說明"]
    return user_text in get_text

user_session = {}
# get text from user who click richmenu
def handle_text_message(event):
    user_id = event.source.user_id
    user_text = event.message.text

    if get_quick_reply_text(user_text):
        if user_text == "操作說明":
            reply_content = TextMessage(text= operation_instruction())
    
        else:
            user_session[user_id] = {'restaurant_type': user_text}
            reply_content = TextMessage(text="請輸入位置！", quickReply=quick_reply_button() )
        
        reply_request =  ReplyMessageRequest(
                replyToken=event.reply_token,
                messages= [reply_content]
            )
        messaging_api.reply_message(reply_request)

# set quick reply button 
def quick_reply_button():
    location_action = LocationAction(
        label= "傳送位置",
        type= "location"
    )

    location_item = QuickReplyItem(
        action= location_action
    )

    quick_reply = QuickReply(items= [location_item])
    return quick_reply


