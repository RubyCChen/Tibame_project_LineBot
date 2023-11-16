import mysql.connector
from mysql.connector import Error
import configparser



# read config and connect to database
def connect_to_db():
    config = configparser.ConfigParser()
    config.read('config.ini')

    db_config = config['database']
    host = db_config.get('host')
    port = db_config.get('port')  
    user = db_config.get('user')
    password = db_config.get('password')
    database = db_config.get('database')

    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            print("Connected to DB.")
        return connection
    
    except Error as e:
        print("Error:", e)
        return None
    
# from database get user needed restaurant info
def get_restaurant_info(restaurant_type, user_longitude, user_latitude, radius):
    conn = connect_to_db()
    if conn is None:
        return None
    
    cursor = conn.cursor()
    query = (
            """
            SELECT *,
                ST_Distance_Sphere(point(longitude, latitude), point(%s, %s)) AS distance
            FROM storeinfo
            WHERE restaurant_type LIKE %s
            AND ST_Distance_Sphere(point(longitude, latitude), point(%s, %s)) <= %s
            AND score > 9;"""
    )
    params = (user_longitude, user_latitude, f"%{restaurant_type}%", user_longitude, user_latitude, radius * 1000)
    cursor.execute(query,params)
    result = cursor.fetchall()
    # print("Get the info: ", result)
    cursor.close()
    conn.close()
    return result 

# design flex message
def flex_message(restaurant_info):
    if not restaurant_info:
        # print("Not Found!!!")
        return None
    
    for restaurant in restaurant_info:
        # print("Processing restaurant:", restaurant)
        restaurant_name = restaurant[1]
        restaurant_type = restaurant[2]
        restaurant_address = restaurant[3]
        restaurant_phone = restaurant[4]
        restaurant_longitude = float(restaurant[5])
        restaurant_latitude = float(restaurant[6])
        restaurant_training_score = float(restaurant[9])
        restaurant_photo = restaurant[10]
        restaurant_website = restaurant[11]
        star_num = min(round(restaurant_training_score),5)

    # according to training score then set the star number
        star = [
            {
                  "type" : "icon",
                  "size" : "sm",
                  "url" : "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
            }
            for _ in range(star_num)
        ] + [
            {
                "type": "icon",
                "size": "sm",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
            }
                for _ in range(5- star_num)
        ]

    # set bubble content
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": restaurant_photo,
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": restaurant_name,
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": star + [
                    {
                        "type": "text",
                        "text": str(restaurant_training_score),
                        "size": "sm",
                        "color": "#999999",
                        "margin" :"md",
                        "flex" :0
                    }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "Place",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                        },
                        {
                            "type": "text",
                            "text": restaurant_address,
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "CALL",
                    "uri": "tel:{}".format(restaurant_phone)
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                    "type": "uri",
                    "label": "WEBSITE",
                    "uri": restaurant_website
                    }
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [],
                    "margin": "sm"
                }
                ],
                "flex": 0
            }
            }

    return bubble
    


