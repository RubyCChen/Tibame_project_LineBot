import configparser
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    RichMenuRequest,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction,
    MessageAction
)

# read channel assess token and channel secert
config = configparser.ConfigParser()
config.read('config.ini')
configuration = Configuration(access_token=config.get('line-bot', 'channel_access_token')) 
handler = WebhookHandler(config.get('line-bot', 'channel_secret')) 

# set header for http request
HEADER = {
    'Content-type': 'image/png',
    'Authorization': F'Bearer {config.get("line-bot", "channel_access_token")}'
}

# design richmenu and define button site
def create_rich_menu():
    return {
        'size' : {'width':2500, 'height': 1686},
        'selected' : True,
        'name' : 'richmenu-v4',
        'chatBarText' : 'Tap to choose',
        'areas' :[
            {
                'bounds': {'x': 666,  'y': 870 , 'width': 512 , 'height': 765}, 
                'action': {'type': 'message', 'text': '排骨飯'}                 
            },
            {
                'bounds': {'x': 664, 'y': 49 , 'width': 512 , 'height': 765}, 
                'action': {'type': 'message', 'text': '壽司'}                
            },
            {
                'bounds': {'x': 1288, 'y': 49 , 'width': 512 , 'height': 765}, 
                'action': {'type': 'message', 'text': '拉麵'}                
            },
            {
                'bounds': {'x': 1288, 'y': 870 , 'width': 512 , 'height': 765}, 
                'action': {'type': 'message', 'text': '義大利麵'}                
            },
            {
                'bounds': {'x': 1913, 'y': 49 , 'width': 512 , 'height': 765}, 
                'action': {'type': 'message', 'text': '漢堡'}                
            },
            {
                'bounds': {'x': 59, 'y': 870 , 'width': 512 , 'height': 7651}, 
                'action': {'type': 'uri', 'uri': 'https://public.tableau.com/app/profile/luna.chen6881/viz/google_16998661926280/dashboard?publish=yes'}                
            },
            {
                'bounds': {'x': 1913, 'y': 870 , 'width': 512 , 'height': 7651}, 
                'action': {'type': 'uri', 'uri': 'https://drive.google.com/drive/folders/1Mfrr7OX2A4CLUP3tG4TmCjLXIsFVSZdN?usp=drive_link'}                
            },
            {
                'bounds': {'x': 59, 'y': 49 , 'width': 512 , 'height': 765}, 
                'action': {'type': 'message', 'text': '操作說明'}                  
            },
        ]
    } 


# define button action
def button_action(action):
    if action['type'] == 'message':
        return MessageAction(text=action.get('text'))
    
    elif action['type'] == 'uri':
        return URIAction(uri=action.get('uri'))
    

# set richmenu as default
def set_menu():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        richmenu = create_rich_menu()
        areas = [
                RichMenuArea(
                bounds=RichMenuBounds(
                    x=info['bounds']['x'],
                    y=info['bounds']['y'],
                    width=info['bounds']['width'],
                    height=info['bounds']['height']
                ),
                action=button_action(info['action'])
            ) for info in richmenu['areas']
        ]

        set_richmenu = RichMenuRequest(
                size=RichMenuSize(
                    width=richmenu['size']['width'],
                    height=richmenu['size']['height']),
                    selected=richmenu['selected'],
                    name=richmenu['chatBarText'],
                    chat_bar_text=richmenu['chatBarText'],
                    areas=areas
                )
        
        richmenu_id = line_bot_api.create_rich_menu(
                rich_menu_request= set_richmenu
            ).rich_menu_id

        with open(r'C:\Users\T14 Gen 3\Desktop\Project\Line\menu06.png', "rb") as f:
                line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=richmenu_id,
                body=bytearray(f.read()),
                _headers={'Content-Type': 'image/png'}
    )

        line_bot_api.set_default_rich_menu(richmenu_id)
        return f"Rich menu created and set as default with ID: {richmenu_id}"




