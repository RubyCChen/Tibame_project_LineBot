import json

resumes = [
    ["簡煒軒", "積極參與科技創新的過程，遠比單純的使用更加充實和有意義。", "https://www.canva.com/design/DAF0Hc-KtI8/950D4FEukvA7ASJEatJFUA/edit?utm_content=DAF0Hc-KtI8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton", "https://scontent.ftpe7-4.fna.fbcdn.net/v/t31.18172-8/24785095_1910387592311069_6556469145402395758_o.jpg?_nc_cat=105&ccb=1-7&_nc_sid=7f8c78&_nc_ohc=WRjHyxuuoqoAX8NnlLI&_nc_ht=scontent.ftpe7-4.fna&oh=00_AfCkAo6DACUGIJvjcIG9c8B9GRzDen_b03sG4Ik3nu2dZQ&oe=6583E2F7"],
    ["鄭淑芬", "最危險的情況是當你不再有新進展。", "https://drive.google.com/drive/folders/14gF4HwV2UNc2fNjBosmtzFe1RrdyiTrZ?usp=drive_link", "https://scontent.ftpe8-1.fna.fbcdn.net/v/t1.6435-9/91328858_3588718974478449_5293131821737836544_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=be3454&_nc_ohc=kz3higmOt18AX9DJR_m&_nc_ht=scontent.ftpe8-1.fna&cb_e2o_trans=q&oh=00_AfCRDPX-u0RIWaLkIRCUuO8ACUrhtPR4AOUEf_67yxdUUQ&oe=6583D836"],
    ["陳品妤", "複雜的事情要簡單做，簡單的事情要認真做，認真的事情要重複做，重複的事情要創造性地做。", "https://drive.google.com/drive/folders/1U_lYZjTnxdzd97ydJ65ADGeE6WKPu47j", "https://scontent.ftpe3-1.fna.fbcdn.net/v/t39.30808-6/405968555_2506335172882532_8960311063142383969_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=5f2048&_nc_ohc=govJPjn5ivkAX87_sBA&_nc_ht=scontent.ftpe3-1.fna&oh=00_AfB07IKIYdTql-WJnob3NqnXWprW9Ybsktwuzy5qb25DCw&oe=65681BF0"],
    ["李承修", "當一個有夢想的人，可以喊累 ，但絕不可以停下前進的腳步。", "https://drive.google.com/drive/folders/1LbMhkaVhv42G4oOo6EpGlEwuqHiOrdCX", "https://scontent.ftpe9-1.fna.fbcdn.net/v/t39.30808-6/406209242_24263778659934556_5367834109052910917_n.jpg?stp=cp0_dst-jpg_e15_fr_q65&_nc_cat=111&ccb=1-7&_nc_sid=5f2048&efg=eyJpIjoidCJ9&_nc_ohc=E81BsLBZwaYAX_6JJAT&tn=r22VWPO14V3JZMya&_nc_ht=scontent.ftpe9-1.fna&oh=00_AfDT-dIuNsAYZWPwQovn-5ke6-BNJIh5cdj8NSqvO__uPA&oe=6566E56A"],
    ["陳彥如", "你不一定要很厲害，才能開始；但你要開始，才能很厲害。", "https://www.canva.com/design/DAF1PWy5aNk/DLV9rUc6XKcGcwDi7lxUVw/view?utm_content=DAF1PWy5aNk&utm_campaign=designshare&utm_medium=link&utm_source=editor", "https://scontent.ftpe9-1.fna.fbcdn.net/v/t39.30808-6/403123035_6790972730984646_353442609620466688_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=5f2048&_nc_ohc=dD9zKXd-Fc8AX9mRYI3&_nc_ht=scontent.ftpe9-1.fna&oh=00_AfBRVzyrJbGN5NzD0Fgr_HsTz88Gj1U48frDjwQWzXz4Rw&oe=65670DC6"]
]

# design flex message
def flex_message_resume(resumes):
    carousel_contents = [ ]

    for resume in resumes:
        name = resume[0]
        text = resume[1]
        resume_url = resume[2]
        resume_photo = resume[3]
        
# set bubble 
        bubble = {
            "type": "bubble",
            "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": resume_photo
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "text",
                    "text": name,
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                    {
                        "type": "text",
                        "text": text,
                        "wrap": True,
                        "color": "#666666",
                        "size": "sm",
                        "flex": 5
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
                    "action": {
                    "type": "uri",
                    "label": "個人履歷",
                    "uri": resume_url
                    }
                }
            ]
        }
    }
        carousel_contents.append(bubble)

    flex_message = {
        "type" : "carousel",
        "contents" : carousel_contents
    }
    
    return flex_message


# if __name__ == "__main__":

#     test = [
#         ("鄭淑芬", " DBA ", "https://drive.google.com/drive/folders/1Mfrr7OX2A4CLUP3tG4TmCjLXIsFVSZdN?usp=drive_link", "https://st.depositphotos.com/2001755/3622/i/450/depositphotos_36220949-stock-photo-beautiful-landscape.jpg "),
        
#         ("陳彥如", " Backend Engineer ", "https://drive.google.com/drive/folders/1Mfrr7OX2A4CLUP3tG4TmCjLXIsFVSZdN?usp=drive_link", "https://drive.google.com/file/d/1fAr4nB8d1kKbugry5iUEszMenvN61f9k/view?usp=drive_link")
#    ]

#     test_flex_message = flex_message_resume(    test 
# )


#     print(json.dumps(test_flex_message, indent=4, ensure_ascii=False))
            




