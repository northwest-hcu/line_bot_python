import requests, json 
    
def getWeatherInfo(cityName):
    fp=open('./secret.json','r',encoding='utf-8')
    data=json.load(fp)

    # 取得したAPIkey
    apiKey = data['openweather_apikey']

    # ベースURL
    baseUrl = "http://api.openweathermap.org/data/2.5/weather…?"

    # URL作成
    completeUrl = baseUrl + "appid=" + apiKey + "&q=" + cityName 

    # レスポンス
    response = requests.get(completeUrl) 

    # レスポンスの内容をJSONフォーマットからPythonフォーマットに変換
    cityData = response.json() 

    # Codが404だと都市名が見つかりませんの意味
    if cityData["cod"] != "404": 
        # print("都市名==>",cityData["name"])
        # print("天気==>",cityData["weather"][0]["description"])
        # print("現在の気温==>",cityData["main"]["temp"] - 273.15,"℃")
        # print("最高気温==>",cityData["main"]["temp_max"] - 273.15,"℃")
        # print("最低気温==>",cityData["main"]["temp_min"] - 273.15,"℃")
        # print("湿度==>",cityData["main"]["humidity"])
        # print("気圧==>",cityData["main"]["pressure"])
        # print("湿度==>",cityData["main"]["humidity"])
        # print("風速==>",cityData["wind"]["speed"])
        ans = "天気：" + str(cityData["weather"][0]["description"]) + "¥n"
        ans = ans + "現在の気温：" + str(cityData["main"]["temp"] - 273.15) + "¥n"
        ans = ans + "最高気温：" + str(cityData["main"]["temp_max"] - 273.15) + "¥n"
        ans = ans + "最低気温：" + str(cityData["main"]["temp_min"] - 273.15) + "¥n"
        ans = ans + "湿度：" + str(cityData["main"]["humidity"])
        ans = ans + "気圧：" + str(cityData["main"]["pressure"])
        ans = ans + "風速：" + str(cityData["wind"]["speed"])
        return ans
    else: 
        # print("都市名がみつかりませんでした。")
        return "都市名がみつかりませんでした."