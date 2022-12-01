from datetime import datetime
import re
from turtle import title
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Article
import math

def homePage(request):   
    if 'city' in request.POST:
        city_input = request.POST['city']
    else:
        city_input = 'Dhaka'
    apikey = 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9'
    request.session['city_name'] = city_input
    location_URL = 'http://dataservice.accuweather.com/locations/v1/cities/search'
    location_PARAMS = {
        'apikey' : 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9',
        'q' : city_input
    }
    location_request = requests.get(url=location_URL, params=location_PARAMS)
    location_response = location_request.json()
    city = location_response[0]['AdministrativeArea']['EnglishName']
    country = location_response[0]['Country']['EnglishName']
    city_key = location_response[0]['Key']
    request.session['city'] = city_key
    weather_URL = 'http://dataservice.accuweather.com/currentconditions/v1/{path}'.format(path=city_key)
    weather_PARAMS = {
        'apikey': 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9'
    }
    weather_request = requests.get(url=weather_URL, params=weather_PARAMS)
    weather_response = weather_request.json()
    description = weather_response[0]['WeatherText']
    icon = weather_response[0]['WeatherIcon']
    temperature = weather_response[0]['Temperature']['Metric']['Value']
    unit = weather_response[0]['Temperature']['Metric']['Unit']
    articles = Article.objects.all()
    
    return render(request, 'init_app/index.html', {'city': city, 
                                                   'country': country, 
                                                   'icon': icon, 
                                                   'description': description, 
                                                   'temp': temperature, 
                                                   'unit': unit,
                                                   'articles': articles})

def articlePage(request):
    articles = Article.objects.values()
    
    return render(request, 'init_app/article_page.html', {'articles': articles})

def todayPage(request):
    city_key = request.session['city']
    today_URL = 'http://dataservice.accuweather.com/currentconditions/v1/{locationKey}'.format(locationKey=city_key)
    today_PARAMS = {
        'apikey' : 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9',
        'details' : True

    }
    today_request = requests.get(url=today_URL, params=today_PARAMS)
    today_response = today_request.json()
    epoch_time = today_response[0]['EpochTime']
    time = datetime.fromtimestamp(epoch_time)
    temperature = today_response[0]['Temperature']['Metric']['Value']
    unit = today_response[0]['Temperature']['Metric']['Unit']
    description = today_response[0]['WeatherText']
    icon = today_response[0]['WeatherIcon']
    real_feel_temperature = today_response[0]['RealFeelTemperature']['Metric']['Value']
    real_feel_unit = today_response[0]['RealFeelTemperature']['Metric']['Unit']
    real_feel_description = today_response[0]['RealFeelTemperature']['Metric']['Phrase']
    wind_speed = today_response[0]['Wind']['Speed']['Metric']['Value']
    wind_speed_unit = today_response[0]['Wind']['Speed']['Metric']['Unit']
    humidity = today_response[0]['RelativeHumidity']
    indoor_humidity = today_response[0]['IndoorRelativeHumidity']
    wind_gust = today_response[0]['WindGust']['Speed']['Metric']['Value']
    wind_gust_unit = today_response[0]['WindGust']['Speed']['Metric']['Unit']
    visibility = today_response[0]['Visibility']['Metric']['Value']
    visibility_unit = today_response[0]['Visibility']['Metric']['Unit']
    cloud_cover = today_response[0]['CloudCover']
    ceiling = today_response[0]['Ceiling']['Metric']['Value']
    ceiling_unit = today_response[0]['Ceiling']['Metric']['Unit']
    pressure = today_response[0]['Pressure']['Metric']['Value']
    pressure_unit = today_response[0]['Pressure']['Metric']['Unit']

    air_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/1day/{location_key}'.format(location_key=city_key)
    air_PARAMS = {
        'apikey': 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9',
        'details': True
    }
    aqi_request = requests.get(url=air_URL, params=air_PARAMS)
    aqi_response = aqi_request.json()
    air_quality = aqi_response['DailyForecasts'][0]['AirAndPollen'][0]['Category']
    day_icon = aqi_response['DailyForecasts'][0]['Day']['Icon']
    icon_text = aqi_response['DailyForecasts'][0]['Day']['IconPhrase']
    day_phrase = aqi_response['DailyForecasts'][0]['Day']['LongPhrase']
    day_wind = aqi_response['DailyForecasts'][0]['Day']['Wind']['Speed']['Value']
    day_wind_direction = aqi_response['DailyForecasts'][0]['Day']['Wind']['Direction']['English']
    day_wind_gust = aqi_response['DailyForecasts'][0]['Day']['WindGust']['Speed']['Value']
    day_wind_gust_direction = aqi_response['DailyForecasts'][0]['Day']['WindGust']['Direction']['English']
    day_precipitation = aqi_response['DailyForecasts'][0]['Day']['PrecipitationProbability']
    day_thunderstorm = aqi_response['DailyForecasts'][0]['Day']['ThunderstormProbability']
    day_rain = aqi_response['DailyForecasts'][0]['Day']['Rain']['Value']
    day_hours_precipitation = aqi_response['DailyForecasts'][0]['Day']['HoursOfPrecipitation']
    day_hours_rain = aqi_response['DailyForecasts'][0]['Day']['HoursOfRain']
    day_cloud_cover = aqi_response['DailyForecasts'][0]['Day']['CloudCover']

    night_icon = aqi_response['DailyForecasts'][0]['Night']['Icon']
    night_icon_text = aqi_response['DailyForecasts'][0]['Night']['IconPhrase']
    night_phrase = aqi_response['DailyForecasts'][0]['Night']['LongPhrase']
    night_wind = aqi_response['DailyForecasts'][0]['Night']['Wind']['Speed']['Value']
    night_wind_direction = aqi_response['DailyForecasts'][0]['Night']['Wind']['Direction']['English']
    night_wind_gust = aqi_response['DailyForecasts'][0]['Night']['WindGust']['Speed']['Value']
    night_wind_gust_direction = aqi_response['DailyForecasts'][0]['Night']['WindGust']['Direction']['English']
    night_precipitation = aqi_response['DailyForecasts'][0]['Night']['PrecipitationProbability']
    night_thunderstorm = aqi_response['DailyForecasts'][0]['Night']['ThunderstormProbability']
    night_rain = aqi_response['DailyForecasts'][0]['Night']['Rain']['Value']
    night_hours_precipitation = aqi_response['DailyForecasts'][0]['Night']['HoursOfPrecipitation']
    night_hours_rain = aqi_response['DailyForecasts'][0]['Night']['HoursOfRain']
    night_cloud_cover = aqi_response['DailyForecasts'][0]['Night']['CloudCover']

    return render(request, 'init_app/today_page.html', {'time': time,
                                                        'temperature': temperature,
                                                        'unit': unit,
                                                        'description': description,
                                                        'icon': icon,
                                                        'real_temperature': real_feel_temperature,
                                                        'real_unit': real_feel_unit,
                                                        'real_description': real_feel_description,
                                                        'wind': wind_speed,
                                                        'wind_unit': wind_speed_unit,
                                                        'humidity': humidity,
                                                        'indoor_humidity': indoor_humidity,
                                                        'wind_gust': wind_gust,
                                                        'wind_gust_unit': wind_gust_unit,
                                                        'visibility': visibility,
                                                        'visibility_unit': visibility_unit,
                                                        'cloud_cover': cloud_cover,
                                                        'ceiling': ceiling,
                                                        'ceiling_unit': ceiling_unit,
                                                        'pressure': pressure,
                                                        'pressure_unit': pressure_unit,
                                                        'air_quality': air_quality,
                                                        'day_icon': day_icon,
                                                        'icon_text': icon_text,
                                                        'day_phrase': day_phrase,
                                                        'day_wind': day_wind,
                                                        'day_wind_direction': day_wind_direction,
                                                        'day_wind_gust': day_wind_gust,
                                                        'day_wind_gust_direction': day_wind_gust_direction,
                                                        'day_precipitation': day_precipitation,
                                                        'day_thunderstorm': day_thunderstorm,
                                                        'day_rain': day_rain,
                                                        'day_hours_precipitation': day_hours_precipitation,
                                                        'day_hours_rain': day_hours_rain,
                                                        'day_cloud_cover': day_cloud_cover,
                                                        'night_icon': day_icon,
                                                        'night_icon_text': night_icon_text,
                                                        'night_phrase': night_phrase,
                                                        'night_wind': night_wind,
                                                        'night_wind_direction': night_wind_direction,
                                                        'night_wind_gust': night_wind_gust,
                                                        'night_wind_gust_direction': night_wind_gust_direction,
                                                        'night_precipitation': night_precipitation,
                                                        'night_thunderstorm': night_thunderstorm,
                                                        'night_rain': night_rain,
                                                        'night_hours_precipitation': night_hours_precipitation,
                                                        'night_hours_rain': night_hours_rain,
                                                        'night_cloud_cover': night_cloud_cover})

def hourlyPage(request):
    city_key = request.session['city']
    hourly_URL = 'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}'.format(location_key=city_key)
    hourly_PARAMS = {
        'apikey': 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9',
        'details': True,
        'metric': True
    }
    hourly_request = requests.get(url=hourly_URL, params=hourly_PARAMS)
    hourly_response = hourly_request.json()
    epoch_time1 = hourly_response[0]['EpochDateTime']
    time1 = datetime.fromtimestamp(epoch_time1).time()
    icon1 = hourly_response[0]['WeatherIcon']
    icon_phrase1 = hourly_response[0]['IconPhrase']
    temperature1 = hourly_response[0]['Temperature']['Value']
    real_temperature1 = hourly_response[0]['RealFeelTemperature']['Value']
    uv1 = hourly_response[0]['UVIndex']
    uv_text1 = hourly_response[0]['UVIndexText']
    wind1 = hourly_response[0]['Wind']['Speed']['Value']
    wind_direction1 = hourly_response[0]['Wind']['Direction']['English']
    wind_gust1 = hourly_response[0]['WindGust']['Speed']['Value']
    humidity1 = hourly_response[0]['RelativeHumidity']
    indoor_humidity1 = hourly_response[0]['IndoorRelativeHumidity']
    dew_point1 = hourly_response[0]['DewPoint']['Value']
    cloud_cover1 = hourly_response[0]['CloudCover']
    rain1 = hourly_response[0]['Rain']['Value']
    visibility1 = hourly_response[0]['Visibility']['Value']
    cloud_ceiling1 = hourly_response[0]['Ceiling']['Value']


    epoch_time2 = hourly_response[1]['EpochDateTime']
    time2 = datetime.fromtimestamp(epoch_time2).time()
    icon2 = hourly_response[1]['WeatherIcon']
    icon_phrase2 = hourly_response[1]['IconPhrase']
    temperature2 = hourly_response[1]['Temperature']['Value']
    real_temperature2 = hourly_response[1]['RealFeelTemperature']['Value']
    uv2 = hourly_response[1]['UVIndex']
    uv_text2 = hourly_response[1]['UVIndexText']
    wind2 = hourly_response[1]['Wind']['Speed']['Value']
    wind_direction2 = hourly_response[1]['Wind']['Direction']['English']
    wind_gust2 = hourly_response[1]['WindGust']['Speed']['Value']
    humidity2 = hourly_response[1]['RelativeHumidity']
    indoor_humidity2 = hourly_response[1]['IndoorRelativeHumidity']
    dew_point2 = hourly_response[1]['DewPoint']['Value']
    cloud_cover2 = hourly_response[1]['CloudCover']
    rain2 = hourly_response[1]['Rain']['Value']
    visibility2 = hourly_response[1]['Visibility']['Value']
    cloud_ceiling2 = hourly_response[1]['Ceiling']['Value']


    epoch_time3 = hourly_response[2]['EpochDateTime']
    time3 = datetime.fromtimestamp(epoch_time3).time()
    icon3 = hourly_response[2]['WeatherIcon']
    icon_phrase3 = hourly_response[2]['IconPhrase']
    temperature3 = hourly_response[2]['Temperature']['Value']
    real_temperature3 = hourly_response[2]['RealFeelTemperature']['Value']
    uv3 = hourly_response[2]['UVIndex']
    uv_text3 = hourly_response[2]['UVIndexText']
    wind3 = hourly_response[2]['Wind']['Speed']['Value']
    wind_direction3 = hourly_response[2]['Wind']['Direction']['English']
    wind_gust3 = hourly_response[2]['WindGust']['Speed']['Value']
    humidity3 = hourly_response[2]['RelativeHumidity']
    indoor_humidity3 = hourly_response[2]['IndoorRelativeHumidity']
    dew_point3 = hourly_response[2]['DewPoint']['Value']
    cloud_cover3 = hourly_response[2]['CloudCover']
    rain3 = hourly_response[2]['Rain']['Value']
    visibility3 = hourly_response[2]['Visibility']['Value']
    cloud_ceiling3 = hourly_response[2]['Ceiling']['Value']

    epoch_time4 = hourly_response[3]['EpochDateTime']
    time4 = datetime.fromtimestamp(epoch_time4).time()
    icon4 = hourly_response[3]['WeatherIcon']
    icon_phrase4 = hourly_response[3]['IconPhrase']
    temperature4 = hourly_response[3]['Temperature']['Value']
    real_temperature4 = hourly_response[3]['RealFeelTemperature']['Value']
    uv4 = hourly_response[3]['UVIndex']
    uv_text4 = hourly_response[3]['UVIndexText']
    wind4 = hourly_response[3]['Wind']['Speed']['Value']
    wind_direction4 = hourly_response[3]['Wind']['Direction']['English']
    wind_gust4 = hourly_response[3]['WindGust']['Speed']['Value']
    humidity4 = hourly_response[3]['RelativeHumidity']
    indoor_humidity4 = hourly_response[3]['IndoorRelativeHumidity']
    dew_point4 = hourly_response[3]['DewPoint']['Value']
    cloud_cover4 = hourly_response[3]['CloudCover']
    rain4 = hourly_response[3]['Rain']['Value']
    visibility4 = hourly_response[3]['Visibility']['Value']
    cloud_ceiling4 = hourly_response[3]['Ceiling']['Value']


    epoch_time5 = hourly_response[4]['EpochDateTime']
    time5 = datetime.fromtimestamp(epoch_time5).time()
    icon5 = hourly_response[4]['WeatherIcon']
    icon_phrase5 = hourly_response[4]['IconPhrase']
    temperature5 = hourly_response[4]['Temperature']['Value']
    real_temperature5 = hourly_response[4]['RealFeelTemperature']['Value']
    uv5 = hourly_response[4]['UVIndex']
    uv_text5 = hourly_response[4]['UVIndexText']
    wind5 = hourly_response[4]['Wind']['Speed']['Value']
    wind_direction5 = hourly_response[4]['Wind']['Direction']['English']
    wind_gust5 = hourly_response[4]['WindGust']['Speed']['Value']
    humidity5 = hourly_response[4]['RelativeHumidity']
    indoor_humidity5 = hourly_response[4]['IndoorRelativeHumidity']
    dew_point5 = hourly_response[4]['DewPoint']['Value']
    cloud_cover5 = hourly_response[4]['CloudCover']
    rain5 = hourly_response[4]['Rain']['Value']
    visibility5 = hourly_response[4]['Visibility']['Value']
    cloud_ceiling5 = hourly_response[4]['Ceiling']['Value']


    epoch_time6 = hourly_response[5]['EpochDateTime']
    time6 = datetime.fromtimestamp(epoch_time6).time()
    icon6 = hourly_response[5]['WeatherIcon']
    icon_phrase6 = hourly_response[5]['IconPhrase']
    temperature6 = hourly_response[5]['Temperature']['Value']
    real_temperature6 = hourly_response[5]['RealFeelTemperature']['Value']
    uv6 = hourly_response[5]['UVIndex']
    uv_text6 = hourly_response[5]['UVIndexText']
    wind6 = hourly_response[5]['Wind']['Speed']['Value']
    wind_direction6 = hourly_response[5]['Wind']['Direction']['English']
    wind_gust6 = hourly_response[5]['WindGust']['Speed']['Value']
    humidity6 = hourly_response[5]['RelativeHumidity']
    indoor_humidity6 = hourly_response[5]['IndoorRelativeHumidity']
    dew_point6 = hourly_response[5]['DewPoint']['Value']
    cloud_cover6 = hourly_response[5]['CloudCover']
    rain6 = hourly_response[5]['Rain']['Value']
    visibility6 = hourly_response[5]['Visibility']['Value']
    cloud_ceiling6 = hourly_response[5]['Ceiling']['Value']


    epoch_time7 = hourly_response[6]['EpochDateTime']
    time7 = datetime.fromtimestamp(epoch_time7).time()
    icon7 = hourly_response[6]['WeatherIcon']
    icon_phrase7 = hourly_response[6]['IconPhrase']
    temperature7 = hourly_response[6]['Temperature']['Value']
    real_temperature7 = hourly_response[6]['RealFeelTemperature']['Value']
    uv7 = hourly_response[6]['UVIndex']
    uv_text7 = hourly_response[6]['UVIndexText']
    wind7 = hourly_response[6]['Wind']['Speed']['Value']
    wind_direction7 = hourly_response[6]['Wind']['Direction']['English']
    wind_gust7 = hourly_response[6]['WindGust']['Speed']['Value']
    humidity7 = hourly_response[6]['RelativeHumidity']
    indoor_humidity7 = hourly_response[6]['IndoorRelativeHumidity']
    dew_point7 = hourly_response[6]['DewPoint']['Value']
    cloud_cover7 = hourly_response[6]['CloudCover']
    rain7 = hourly_response[6]['Rain']['Value']
    visibility7 = hourly_response[6]['Visibility']['Value']
    cloud_ceiling7 = hourly_response[6]['Ceiling']['Value']


    epoch_time8 = hourly_response[7]['EpochDateTime']
    time8 = datetime.fromtimestamp(epoch_time8).time()
    icon8 = hourly_response[7]['WeatherIcon']
    icon_phrase8 = hourly_response[7]['IconPhrase']
    temperature8 = hourly_response[7]['Temperature']['Value']
    real_temperature8 = hourly_response[7]['RealFeelTemperature']['Value']
    uv8 = hourly_response[7]['UVIndex']
    uv_text8 = hourly_response[7]['UVIndexText']
    wind8 = hourly_response[7]['Wind']['Speed']['Value']
    wind_direction8 = hourly_response[7]['Wind']['Direction']['English']
    wind_gust8 = hourly_response[7]['WindGust']['Speed']['Value']
    humidity8 = hourly_response[7]['RelativeHumidity']
    indoor_humidity8 = hourly_response[7]['IndoorRelativeHumidity']
    dew_point8 = hourly_response[7]['DewPoint']['Value']
    cloud_cover8 = hourly_response[7]['CloudCover']
    rain8 = hourly_response[7]['Rain']['Value']
    visibility8 = hourly_response[7]['Visibility']['Value']
    cloud_ceiling8 = hourly_response[7]['Ceiling']['Value']


    epoch_time9 = hourly_response[8]['EpochDateTime']
    time9 = datetime.fromtimestamp(epoch_time9).time()
    icon9 = hourly_response[8]['WeatherIcon']
    icon_phrase9 = hourly_response[8]['IconPhrase']
    temperature9 = hourly_response[8]['Temperature']['Value']
    real_temperature9 = hourly_response[8]['RealFeelTemperature']['Value']
    uv9 = hourly_response[8]['UVIndex']
    uv_text9 = hourly_response[8]['UVIndexText']
    wind9 = hourly_response[8]['Wind']['Speed']['Value']
    wind_direction9 = hourly_response[8]['Wind']['Direction']['English']
    wind_gust9 = hourly_response[8]['WindGust']['Speed']['Value']
    humidity9 = hourly_response[8]['RelativeHumidity']
    indoor_humidity9 = hourly_response[8]['IndoorRelativeHumidity']
    dew_point9 = hourly_response[8]['DewPoint']['Value']
    cloud_cover9 = hourly_response[8]['CloudCover']
    rain9 = hourly_response[8]['Rain']['Value']
    visibility9 = hourly_response[8]['Visibility']['Value']
    cloud_ceiling9 = hourly_response[8]['Ceiling']['Value']


    epoch_time10 = hourly_response[9]['EpochDateTime']
    time10 = datetime.fromtimestamp(epoch_time10).time()
    icon10 = hourly_response[9]['WeatherIcon']
    icon_phrase10 = hourly_response[9]['IconPhrase']
    temperature10 = hourly_response[9]['Temperature']['Value']
    real_temperature10 = hourly_response[9]['RealFeelTemperature']['Value']
    uv10 = hourly_response[9]['UVIndex']
    uv_text10 = hourly_response[9]['UVIndexText']
    wind10 = hourly_response[9]['Wind']['Speed']['Value']
    wind_direction10 = hourly_response[9]['Wind']['Direction']['English']
    wind_gust10 = hourly_response[9]['WindGust']['Speed']['Value']
    humidity10 = hourly_response[9]['RelativeHumidity']
    indoor_humidity10 = hourly_response[9]['IndoorRelativeHumidity']
    dew_point10 = hourly_response[9]['DewPoint']['Value']
    cloud_cover10 = hourly_response[9]['CloudCover']
    rain10 = hourly_response[9]['Rain']['Value']
    visibility10 = hourly_response[9]['Visibility']['Value']
    cloud_ceiling10 = hourly_response[9]['Ceiling']['Value']


    epoch_time11 = hourly_response[10]['EpochDateTime']
    time11 = datetime.fromtimestamp(epoch_time11).time()
    icon11 = hourly_response[10]['WeatherIcon']
    icon_phrase11 = hourly_response[10]['IconPhrase']
    temperature11 = hourly_response[10]['Temperature']['Value']
    real_temperature11 = hourly_response[10]['RealFeelTemperature']['Value']
    uv11 = hourly_response[10]['UVIndex']
    uv_text11 = hourly_response[10]['UVIndexText']
    wind11 = hourly_response[10]['Wind']['Speed']['Value']
    wind_direction11 = hourly_response[10]['Wind']['Direction']['English']
    wind_gust11 = hourly_response[10]['WindGust']['Speed']['Value']
    humidity11 = hourly_response[10]['RelativeHumidity']
    indoor_humidity11 = hourly_response[10]['IndoorRelativeHumidity']
    dew_point11 = hourly_response[10]['DewPoint']['Value']
    cloud_cover11 = hourly_response[10]['CloudCover']
    rain11 = hourly_response[10]['Rain']['Value']
    visibility11 = hourly_response[10]['Visibility']['Value']
    cloud_ceiling11 = hourly_response[10]['Ceiling']['Value']


    epoch_time12 = hourly_response[11]['EpochDateTime']
    time12 = datetime.fromtimestamp(epoch_time12).time()
    icon12 = hourly_response[11]['WeatherIcon']
    icon_phrase12 = hourly_response[11]['IconPhrase']
    temperature12 = hourly_response[11]['Temperature']['Value']
    real_temperature12 = hourly_response[11]['RealFeelTemperature']['Value']
    uv12 = hourly_response[11]['UVIndex']
    uv_text12 = hourly_response[11]['UVIndexText']
    wind12 = hourly_response[11]['Wind']['Speed']['Value']
    wind_direction12 = hourly_response[11]['Wind']['Direction']['English']
    wind_gust12 = hourly_response[11]['WindGust']['Speed']['Value']
    humidity12 = hourly_response[11]['RelativeHumidity']
    indoor_humidity12 = hourly_response[11]['IndoorRelativeHumidity']
    dew_point12 = hourly_response[11]['DewPoint']['Value']
    cloud_cover12 = hourly_response[11]['CloudCover']
    rain12 = hourly_response[11]['Rain']['Value']
    visibility12 = hourly_response[11]['Visibility']['Value']
    cloud_ceiling12 = hourly_response[11]['Ceiling']['Value']

    return render(request, 'init_app/hourly_page.html', {'time1': time1,
                                                         'icon1': icon1,
                                                         'icon_phrase1': icon_phrase1,
                                                         'temperature1': temperature1,
                                                         'real_temperature1': real_temperature1,
                                                         'uv1': uv1,
                                                         'uv_text1': uv_text1,
                                                         'wind1': wind1,
                                                         'wind_direction1': wind_direction1,
                                                         'wind_gust1': wind_gust1,
                                                         'humidity1': humidity1,
                                                         'indoor_humidity1': indoor_humidity1,
                                                         'dew_point1': dew_point1,
                                                         'cloud_cover1': cloud_cover1,
                                                         'rain1': rain1,
                                                         'visibility1': visibility1,
                                                         'cloud_ceiling1': cloud_ceiling1,
                                                         'time2': time2,
                                                         'icon2': icon2,
                                                         'icon_phrase2': icon_phrase2,
                                                         'temperature2': temperature2,
                                                         'real_temperature2': real_temperature2,
                                                         'uv2': uv2,
                                                         'uv_text2': uv_text2,
                                                         'wind2': wind2,
                                                         'wind_direction2': wind_direction2,
                                                         'wind_gust2': wind_gust2,
                                                         'humidity2': humidity2,
                                                         'indoor_humidity2': indoor_humidity2,
                                                         'dew_point2': dew_point2,
                                                         'cloud_cover2': cloud_cover2,
                                                         'rain2': rain2,
                                                         'visibility2': visibility2,
                                                         'cloud_ceiling2': cloud_ceiling2,
                                                         'time3': time3,
                                                         'icon3': icon3,
                                                         'icon_phrase3': icon_phrase3,
                                                         'temperature3': temperature3,
                                                         'real_temperature3': real_temperature3,
                                                         'uv3': uv3,
                                                         'uv_text3': uv_text3,
                                                         'wind3': wind3,
                                                         'wind_direction3': wind_direction3,
                                                         'wind_gust3': wind_gust3,
                                                         'humidity3': humidity3,
                                                         'indoor_humidity3': indoor_humidity3,
                                                         'dew_point3': dew_point3,
                                                         'cloud_cover3': cloud_cover3,
                                                         'rain3': rain3,
                                                         'visibility3': visibility3,
                                                         'cloud_ceiling3': cloud_ceiling3,
                                                         'time4': time4,
                                                         'icon4': icon4,
                                                         'icon_phrase4': icon_phrase4,
                                                         'temperature4': temperature4,
                                                         'real_temperature4': real_temperature4,
                                                         'uv4': uv4,
                                                         'uv_text4': uv_text4,
                                                         'wind4': wind4,
                                                         'wind_direction4': wind_direction4,
                                                         'wind_gust4': wind_gust4,
                                                         'humidity4': humidity4,
                                                         'indoor_humidity4': indoor_humidity4,
                                                         'dew_point4': dew_point4,
                                                         'cloud_cover4': cloud_cover4,
                                                         'rain4': rain4,
                                                         'visibility4': visibility4,
                                                         'cloud_ceiling4': cloud_ceiling4,
                                                         'time5': time5,
                                                         'icon5': icon5,
                                                         'icon_phrase5': icon_phrase5,
                                                         'temperature5': temperature5,
                                                         'real_temperature5': real_temperature5,
                                                         'uv5': uv5,
                                                         'uv_text5': uv_text5,
                                                         'wind5': wind5,
                                                         'wind_direction5': wind_direction5,
                                                         'wind_gust5': wind_gust5,
                                                         'humidity5': humidity5,
                                                         'indoor_humidity5': indoor_humidity5,
                                                         'dew_point5': dew_point5,
                                                         'cloud_cover5': cloud_cover5,
                                                         'rain5': rain5,
                                                         'visibility5': visibility5,
                                                         'cloud_ceiling5': cloud_ceiling5,
                                                         'time6': time6,
                                                         'icon6': icon6,
                                                         'icon_phrase6': icon_phrase6,
                                                         'temperature6': temperature6,
                                                         'real_temperature6': real_temperature6,
                                                         'uv6': uv6,
                                                         'uv_text6': uv_text6,
                                                         'wind6': wind6,
                                                         'wind_direction6': wind_direction6,
                                                         'wind_gust6': wind_gust6,
                                                         'humidity6': humidity6,
                                                         'indoor_humidity6': indoor_humidity6,
                                                         'dew_point6': dew_point6,
                                                         'cloud_cover6': cloud_cover6,
                                                         'rain6': rain6,
                                                         'visibility6': visibility6,
                                                         'cloud_ceiling6': cloud_ceiling6,
                                                         'time7': time7,
                                                         'icon7': icon7,
                                                         'icon_phrase7': icon_phrase7,
                                                         'temperature7': temperature7,
                                                         'real_temperature7': real_temperature7,
                                                         'uv7': uv7,
                                                         'uv_text7': uv_text7,
                                                         'wind7': wind7,
                                                         'wind_direction7': wind_direction7,
                                                         'wind_gust7': wind_gust7,
                                                         'humidity7': humidity7,
                                                         'indoor_humidity7': indoor_humidity7,
                                                         'dew_point7': dew_point7,
                                                         'cloud_cover7': cloud_cover7,
                                                         'rain7': rain7,
                                                         'visibility7': visibility7,
                                                         'cloud_ceiling7': cloud_ceiling7,
                                                         'time8': time8,
                                                         'icon8': icon8,
                                                         'icon_phrase8': icon_phrase8,
                                                         'temperature8': temperature8,
                                                         'real_temperature8': real_temperature8,
                                                         'uv8': uv8,
                                                         'uv_text8': uv_text8,
                                                         'wind8': wind8,
                                                         'wind_direction8': wind_direction8,
                                                         'wind_gust8': wind_gust8,
                                                         'humidity8': humidity8,
                                                         'indoor_humidity8': indoor_humidity8,
                                                         'dew_point8': dew_point8,
                                                         'cloud_cover8': cloud_cover8,
                                                         'rain8': rain8,
                                                         'visibility8': visibility8,
                                                         'cloud_ceiling8': cloud_ceiling8,
                                                         'time9': time9,
                                                         'icon9': icon9,
                                                         'icon_phrase9': icon_phrase9,
                                                         'temperature9': temperature9,
                                                         'real_temperature9': real_temperature9,
                                                         'uv9': uv9,
                                                         'uv_text9': uv_text9,
                                                         'wind9': wind9,
                                                         'wind_direction9': wind_direction9,
                                                         'wind_gust9': wind_gust9,
                                                         'humidity9': humidity9,
                                                         'indoor_humidity9': indoor_humidity9,
                                                         'dew_point9': dew_point9,
                                                         'cloud_cover9': cloud_cover9,
                                                         'rain9': rain9,
                                                         'visibility9': visibility9,
                                                         'cloud_ceiling9': cloud_ceiling9,
                                                         'time10': time10,
                                                         'icon10': icon10,
                                                         'icon_phrase10': icon_phrase10,
                                                         'temperature10': temperature10,
                                                         'real_temperature10': real_temperature10,
                                                         'uv10': uv10,
                                                         'uv_text10': uv_text10,
                                                         'wind10': wind10,
                                                         'wind_direction10': wind_direction10,
                                                         'wind_gust10': wind_gust10,
                                                         'humidity10': humidity10,
                                                         'indoor_humidity10': indoor_humidity10,
                                                         'dew_point10': dew_point10,
                                                         'cloud_cover10': cloud_cover10,
                                                         'rain10': rain10,
                                                         'visibility10': visibility10,
                                                         'cloud_ceiling10': cloud_ceiling10,
                                                         'time11': time11,
                                                         'icon11': icon11,
                                                         'icon_phrase11': icon_phrase11,
                                                         'temperature11': temperature11,
                                                         'real_temperature11': real_temperature11,
                                                         'uv11': uv11,
                                                         'uv_text11': uv_text11,
                                                         'wind11': wind11,
                                                         'wind_direction11': wind_direction11,
                                                         'wind_gust11': wind_gust11,
                                                         'humidity11': humidity11,
                                                         'indoor_humidity11': indoor_humidity11,
                                                         'dew_point11': dew_point11,
                                                         'cloud_cover11': cloud_cover11,
                                                         'rain11': rain11,
                                                         'visibility11': visibility11,
                                                         'cloud_ceiling11': cloud_ceiling11,
                                                         'time12': time12,
                                                         'icon12': icon12,
                                                         'icon_phrase12': icon_phrase12,
                                                         'temperature12': temperature12,
                                                         'real_temperature12': real_temperature12,
                                                         'uv12': uv12,
                                                         'uv_text12': uv_text12,
                                                         'wind12': wind12,
                                                         'wind_direction12': wind_direction12,
                                                         'wind_gust12': wind_gust12,
                                                         'humidity12': humidity12,
                                                         'indoor_humidity12': indoor_humidity12,
                                                         'dew_point12': dew_point12,
                                                         'cloud_cover12': cloud_cover12,
                                                         'rain12': rain12,
                                                         'visibility12': visibility12,
                                                         'cloud_ceiling12': cloud_ceiling12})


def dailyPage(request):
    city_key = request.session['city']
    current_URL = 'http://dataservice.accuweather.com/currentconditions/v1/{location_key}'.format(location_key=city_key)
    current_PARAMS = {
        'apikey': 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9'
    }
    current_request = requests.get(url=current_URL, params=current_PARAMS)
    current_response = current_request.json()
    isDayTime = current_response[0]['IsDayTime']

    day_URL = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}'.format(location_key=city_key)
    day_PARAMS = {
        'apikey': 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9',
        'details': True,
        'metric': True
    }
    day_request = requests.get(url=day_URL, params=day_PARAMS)
    day_response = day_request.json()
    epoch_date1 = day_response['DailyForecasts'][0]['EpochDate']
    date1 = datetime.fromtimestamp(epoch_date1)
    timeline1 = date1.strftime('%B %d')
    day1_week = date1.strftime('%a')
    day1_date = date1.strftime('%m/%d')
    min_temp1 = day_response['DailyForecasts'][0]['Temperature']['Minimum']['Value']
    max_temp1 = day_response['DailyForecasts'][0]['Temperature']['Maximum']['Value']
    min_temp_int1 = math.ceil(min_temp1)
    max_temp_int1 = math.ceil(max_temp1)
    if isDayTime:
        icon1 = day_response['DailyForecasts'][0]['Day']['Icon']
        phrase1 = day_response['DailyForecasts'][0]['Day']['ShortPhrase']
        precipitation_probability1 = day_response['DailyForecasts'][0]['Day']['PrecipitationProbability']
    else:
        icon1 = day_response['DailyForecasts'][0]['Night']['Icon']
        phrase1 = day_response['DailyForecasts'][0]['Night']['ShortPhrase']
        precipitation_probability1 = day_response['DailyForecasts'][0]['Night']['PrecipitationProbability']

    epoch_date2 = day_response['DailyForecasts'][1]['EpochDate']
    date2 = datetime.fromtimestamp(epoch_date2)
    day2_week = date2.strftime('%a')
    day2_date = date2.strftime('%m/%d')
    min_temp2 = day_response['DailyForecasts'][1]['Temperature']['Minimum']['Value']
    max_temp2 = day_response['DailyForecasts'][1]['Temperature']['Maximum']['Value']
    min_temp_int2 = math.ceil(min_temp2)
    max_temp_int2 = math.ceil(max_temp2)
    if isDayTime:
        icon2 = day_response['DailyForecasts'][1]['Day']['Icon']
        phrase2 = day_response['DailyForecasts'][1]['Day']['ShortPhrase']
        precipitation_probability2 = day_response['DailyForecasts'][1]['Day']['PrecipitationProbability']
    else:
        icon2 = day_response['DailyForecasts'][1]['Night']['Icon']
        phrase2 = day_response['DailyForecasts'][1]['Night']['ShortPhrase']
        precipitation_probability2 = day_response['DailyForecasts'][1]['Night']['PrecipitationProbability']
    
    epoch_date3 = day_response['DailyForecasts'][2]['EpochDate']
    date3 = datetime.fromtimestamp(epoch_date3)
    day3_week = date3.strftime('%a')
    day3_date = date3.strftime('%m/%d')
    min_temp3 = day_response['DailyForecasts'][2]['Temperature']['Minimum']['Value']
    max_temp3 = day_response['DailyForecasts'][2]['Temperature']['Maximum']['Value']
    min_temp_int3 = math.ceil(min_temp3)
    max_temp_int3 = math.ceil(max_temp3)
    if isDayTime:
        icon3 = day_response['DailyForecasts'][2]['Day']['Icon']
        phrase3 = day_response['DailyForecasts'][2]['Day']['ShortPhrase']
        precipitation_probability3 = day_response['DailyForecasts'][2]['Day']['PrecipitationProbability']
    else:
        icon3 = day_response['DailyForecasts'][2]['Night']['Icon']
        phrase3 = day_response['DailyForecasts'][2]['Night']['ShortPhrase']
        precipitation_probability3 = day_response['DailyForecasts'][2]['Night']['PrecipitationProbability']
    
    epoch_date4 = day_response['DailyForecasts'][3]['EpochDate']
    date4 = datetime.fromtimestamp(epoch_date4)
    day4_week = date4.strftime('%a')
    day4_date = date4.strftime('%m/%d')
    min_temp4 = day_response['DailyForecasts'][3]['Temperature']['Minimum']['Value']
    max_temp4 = day_response['DailyForecasts'][3]['Temperature']['Maximum']['Value']
    min_temp_int4 = math.ceil(min_temp4)
    max_temp_int4 = math.ceil(max_temp4)
    if isDayTime:
        icon4 = day_response['DailyForecasts'][3]['Day']['Icon']
        phrase4 = day_response['DailyForecasts'][3]['Day']['ShortPhrase']
        precipitation_probability4 = day_response['DailyForecasts'][3]['Day']['PrecipitationProbability']
    else:
        icon4 = day_response['DailyForecasts'][3]['Night']['Icon']
        phrase4 = day_response['DailyForecasts'][3]['Night']['ShortPhrase']
        precipitation_probability4 = day_response['DailyForecasts'][3]['Night']['PrecipitationProbability']
    
    epoch_date5 = day_response['DailyForecasts'][4]['EpochDate']
    date5 = datetime.fromtimestamp(epoch_date5)
    timeline2 = date5.strftime('%B %d')
    day5_week = date5.strftime('%a')
    day5_date = date5.strftime('%m/%d')
    min_temp5 = day_response['DailyForecasts'][4]['Temperature']['Minimum']['Value']
    max_temp5 = day_response['DailyForecasts'][4]['Temperature']['Maximum']['Value']
    min_temp_int5 = math.ceil(min_temp5)
    max_temp_int5 = math.ceil(max_temp5)
    if isDayTime:
        icon5 = day_response['DailyForecasts'][4]['Day']['Icon']
        phrase5 = day_response['DailyForecasts'][4]['Day']['ShortPhrase']
        precipitation_probability5 = day_response['DailyForecasts'][4]['Day']['PrecipitationProbability']
    else:
        icon5 = day_response['DailyForecasts'][4]['Night']['Icon']
        phrase5 = day_response['DailyForecasts'][4]['Night']['ShortPhrase']
        precipitation_probability5 = day_response['DailyForecasts'][4]['Night']['PrecipitationProbability']

    return render(request, 'init_app/daily_page.html', {'timeline1': timeline1,
                                                        'day1_week': day1_week,
                                                        'day1_date': day1_date,
                                                        'min_temp1': min_temp_int1,
                                                        'max_temp1': max_temp_int1,
                                                        'icon1': icon1,
                                                        'phrase1': phrase1,
                                                        'precipitation_probability1': precipitation_probability1,
                                                        'day2_week': day2_week,
                                                        'day2_date': day2_date,
                                                        'min_temp2': min_temp_int2,
                                                        'max_temp2': max_temp_int2,
                                                        'icon2': icon2,
                                                        'phrase2': phrase2,
                                                        'precipitation_probability2': precipitation_probability2,
                                                        'day3_week': day3_week,
                                                        'day3_date': day3_date,
                                                        'min_temp3': min_temp_int3,
                                                        'max_temp3': max_temp_int3,
                                                        'icon3': icon3,
                                                        'phrase3': phrase3,
                                                        'precipitation_probability3': precipitation_probability3,
                                                        'day4_week': day4_week,
                                                        'day4_date': day4_date,
                                                        'min_temp4': min_temp_int4,
                                                        'max_temp4': max_temp_int4,
                                                        'icon4': icon4,
                                                        'phrase4': phrase4,
                                                        'precipitation_probability4': precipitation_probability4,
                                                        'timeline2': timeline2,
                                                        'day5_week': day5_week,
                                                        'day5_date': day5_date,
                                                        'min_temp5': min_temp_int5,
                                                        'max_temp5': max_temp_int5,
                                                        'icon5': icon5,
                                                        'phrase5': phrase5,
                                                        'precipitation_probability5': precipitation_probability5})

def healthPage(request):
    city_key = request.session['city']
    url = 'http://dataservice.accuweather.com/indices/v1/daily/1day/{location_key}'.format(location_key=city_key)
    params = {
        'apikey': 'MnYKNvT2sM5OeIEB5lwPZiENRukHHAk9',
        'details': True
    }
    health_request = requests.get(url=url, params=params)
    health_response = health_request.json()
    arthritis = health_response[22]['Category']
    arthritis_text = health_response[22]['Text']
    sinus = health_response[31]['Category']
    sinus_text = health_response[31]['Text']
    cold = health_response[26]['Category']
    cold_text = health_response[26]['Text']
    flu = health_response[27]['Category']
    flu_text = health_response[27]['Text']
    migraine = health_response[28]['Category']
    migraine_text = health_response[28]['Text']
    asthma = health_response[24]['Category']
    asthma_text = health_response[24]['Text']

    fishing = health_response[14]['Category']
    fishing_text = health_response[14]['Text']
    running = health_response[2]['Category']
    running_text = health_response[2]['Text']
    golf = health_response[6]['Category']
    golf_text = health_response[6]['Text']
    biking = health_response[5]['Category']
    biking_text = health_response[5]['Text']
    beach = health_response[11]['Category']
    beach_text = health_response[11]['Text']
    stargazing = health_response[13]['Category']
    stargazing_text = health_response[13]['Text']
    hiking = health_response[4]['Category']
    hiking_text = health_response[4]['Text']

    flying = health_response[32]['Category']
    flying_text = health_response[32]['Text']
    driving = health_response[38]['Category']
    driving_text = health_response[38]['Text']

    lawn_mowing = health_response[29]['Category']
    lawn_mowing_text = health_response[29]['Text']
    composting = health_response[36]['Category']
    composting_text = health_response[36]['Text']
    outdoor = health_response[30]['Category']
    outdoor_text = health_response[30]['Text']

    mosquito = health_response[18]['Category']
    mosquito_text = health_response[18]['Text']

    dust = health_response[19]['Category']
    dust_text = health_response[19]['Text']

    return render(request, 'init_app/health&activity.html', {'arthritis': arthritis, 'arthritis_text': arthritis_text,
                                                             'sinus': sinus, 'sinus_text': sinus_text,
                                                             'cold': cold, 'cold_text': cold_text,
                                                             'flu': flu, 'flu_text': flu_text,
                                                             'migraine': migraine, 'migraine_text': migraine_text,
                                                             'asthma': asthma, 'asthma_text': asthma_text,
                                                             'fishing': fishing, 'fishing_text': fishing_text,
                                                             'running': running, 'running_text': running_text,
                                                             'golf': golf, 'golf_text': golf_text,
                                                             'biking': biking, 'biking_text': biking_text,
                                                             'beach': beach, 'beach_text': beach_text,
                                                             'stargazing': stargazing, 'stargazing_text': stargazing_text,
                                                             'hiking': hiking, 'hiking_text': hiking_text,
                                                             'flying': flying, 'flying_text': flying_text,
                                                             'driving': driving, 'driving_text': driving_text,
                                                             'lawn_mowing': lawn_mowing, 'lawn_mowing_text': lawn_mowing_text,
                                                             'composting': composting, 'composting_text': composting_text,
                                                             'outdoor': outdoor, 'outdoor_text': outdoor_text,
                                                             'mosquito': mosquito, 'mosquito_text': mosquito_text,
                                                             'dust': dust, 'dust_text': dust_text})

def minutePage(request):
    city = request.session['city_name']
    minute_url = 'http://api.weatherbit.io/v2.0/forecast/minutely'
    minute_params = {
        'key': '4768ca6b7e584248a7a05526647cc714',
        'city': city
    }
    minute_request = requests.get(url=minute_url, params=minute_params)
    minute_response = minute_request.json()
    ts1 = minute_response['data'][0]['ts']
    time1 = datetime.fromtimestamp(ts1).time()
    date1 = datetime.fromtimestamp(ts1).date()
    prec1 = minute_response['data'][0]['precip']
    
    ts2 = minute_response['data'][1]['ts']
    time2 = datetime.fromtimestamp(ts2).time()
    date2 = datetime.fromtimestamp(ts2).date()
    prec2 = minute_response['data'][1]['precip']

    ts3 = minute_response['data'][2]['ts']
    time3 = datetime.fromtimestamp(ts3).time()
    date3 = datetime.fromtimestamp(ts3).date()
    prec3 = minute_response['data'][2]['precip']

    ts4 = minute_response['data'][3]['ts']
    time4 = datetime.fromtimestamp(ts4).time()
    date4 = datetime.fromtimestamp(ts4).date()
    prec4 = minute_response['data'][3]['precip']

    ts5 = minute_response['data'][4]['ts']
    time5 = datetime.fromtimestamp(ts5).time()
    date5 = datetime.fromtimestamp(ts5).date()
    prec5 = minute_response['data'][4]['precip']

    ts6 = minute_response['data'][5]['ts']
    time6 = datetime.fromtimestamp(ts6).time()
    date6 = datetime.fromtimestamp(ts6).date()
    prec6 = minute_response['data'][5]['precip']

    ts7 = minute_response['data'][6]['ts']
    time7 = datetime.fromtimestamp(ts7).time()
    date7 = datetime.fromtimestamp(ts7).date()
    prec7 = minute_response['data'][6]['precip']

    ts8 = minute_response['data'][7]['ts']
    time8 = datetime.fromtimestamp(ts8).time()
    date8 = datetime.fromtimestamp(ts8).date()
    prec8 = minute_response['data'][7]['precip']

    ts9 = minute_response['data'][8]['ts']
    time9 = datetime.fromtimestamp(ts9).time()
    date9 = datetime.fromtimestamp(ts9).date()
    prec9 = minute_response['data'][8]['precip']

    ts10 = minute_response['data'][9]['ts']
    time10 = datetime.fromtimestamp(ts10).time()
    date10 = datetime.fromtimestamp(ts10).date()
    prec10 = minute_response['data'][9]['precip']

    ts11 = minute_response['data'][10]['ts']
    time11 = datetime.fromtimestamp(ts11).time()
    date11 = datetime.fromtimestamp(ts11).date()
    prec11 = minute_response['data'][10]['precip']

    ts12 = minute_response['data'][11]['ts']
    time12 = datetime.fromtimestamp(ts12).time()
    date12 = datetime.fromtimestamp(ts12).date()
    prec12 = minute_response['data'][11]['precip']

    ts13 = minute_response['data'][12]['ts']
    time13 = datetime.fromtimestamp(ts13).time()
    date13 = datetime.fromtimestamp(ts13).date()
    prec13 = minute_response['data'][12]['precip']

    ts14 = minute_response['data'][13]['ts']
    time14 = datetime.fromtimestamp(ts14).time()
    date14 = datetime.fromtimestamp(ts14).date()
    prec14 = minute_response['data'][13]['precip']

    ts15 = minute_response['data'][14]['ts']
    time15 = datetime.fromtimestamp(ts15).time()
    date15 = datetime.fromtimestamp(ts15).date()
    prec15 = minute_response['data'][14]['precip']

    ts16 = minute_response['data'][15]['ts']
    time16 = datetime.fromtimestamp(ts16).time()
    date16 = datetime.fromtimestamp(ts16).date()
    prec16 = minute_response['data'][15]['precip']

    ts17 = minute_response['data'][16]['ts']
    time17 = datetime.fromtimestamp(ts17).time()
    date17 = datetime.fromtimestamp(ts17).date()
    prec17 = minute_response['data'][16]['precip']

    ts18 = minute_response['data'][17]['ts']
    time18 = datetime.fromtimestamp(ts18).time()
    date18 = datetime.fromtimestamp(ts18).date()
    prec18 = minute_response['data'][17]['precip']

    ts19 = minute_response['data'][18]['ts']
    time19 = datetime.fromtimestamp(ts19).time()
    date19 = datetime.fromtimestamp(ts19).date()
    prec19 = minute_response['data'][18]['precip']

    ts20 = minute_response['data'][19]['ts']
    time20 = datetime.fromtimestamp(ts20).time()
    date20 = datetime.fromtimestamp(ts20).date()
    prec20 = minute_response['data'][19]['precip']

    ts21 = minute_response['data'][20]['ts']
    time21 = datetime.fromtimestamp(ts21).time()
    date21 = datetime.fromtimestamp(ts21).date()
    prec21 = minute_response['data'][20]['precip']

    ts22 = minute_response['data'][21]['ts']
    time22 = datetime.fromtimestamp(ts22).time()
    date22 = datetime.fromtimestamp(ts22).date()
    prec22 = minute_response['data'][21]['precip']

    ts23 = minute_response['data'][22]['ts']
    time23 = datetime.fromtimestamp(ts23).time()
    date23 = datetime.fromtimestamp(ts23).date()
    prec23 = minute_response['data'][22]['precip']

    ts24 = minute_response['data'][23]['ts']
    time24 = datetime.fromtimestamp(ts24).time()
    date24 = datetime.fromtimestamp(ts24).date()
    prec24 = minute_response['data'][23]['precip']

    ts25 = minute_response['data'][24]['ts']
    time25 = datetime.fromtimestamp(ts25).time()
    date25 = datetime.fromtimestamp(ts25).date()
    prec25 = minute_response['data'][24]['precip']

    ts26 = minute_response['data'][25]['ts']
    time26 = datetime.fromtimestamp(ts26).time()
    date26 = datetime.fromtimestamp(ts26).date()
    prec26 = minute_response['data'][25]['precip']

    ts27 = minute_response['data'][26]['ts']
    time27 = datetime.fromtimestamp(ts27).time()
    date27 = datetime.fromtimestamp(ts27).date()
    prec27 = minute_response['data'][26]['precip']

    ts28 = minute_response['data'][27]['ts']
    time28 = datetime.fromtimestamp(ts28).time()
    date28 = datetime.fromtimestamp(ts28).date()
    prec28 = minute_response['data'][27]['precip']

    ts29 = minute_response['data'][28]['ts']
    time29 = datetime.fromtimestamp(ts29).time()
    date29 = datetime.fromtimestamp(ts29).date()
    prec29 = minute_response['data'][28]['precip']

    ts30 = minute_response['data'][29]['ts']
    time30 = datetime.fromtimestamp(ts30).time()
    date30 = datetime.fromtimestamp(ts30).date()
    prec30 = minute_response['data'][29]['precip']

    ts31 = minute_response['data'][30]['ts']
    time31 = datetime.fromtimestamp(ts31).time()
    date31 = datetime.fromtimestamp(ts31).date()
    prec31 = minute_response['data'][30]['precip']

    ts32 = minute_response['data'][31]['ts']
    time32 = datetime.fromtimestamp(ts32).time()
    date32 = datetime.fromtimestamp(ts32).date()
    prec32 = minute_response['data'][31]['precip']

    ts33 = minute_response['data'][32]['ts']
    time33 = datetime.fromtimestamp(ts33).time()
    date33 = datetime.fromtimestamp(ts33).date()
    prec33 = minute_response['data'][32]['precip']

    ts34 = minute_response['data'][33]['ts']
    time34 = datetime.fromtimestamp(ts34).time()
    date34 = datetime.fromtimestamp(ts34).date()
    prec34 = minute_response['data'][33]['precip']
    
    ts35 = minute_response['data'][34]['ts']
    time35 = datetime.fromtimestamp(ts35).time()
    date35 = datetime.fromtimestamp(ts35).date()
    prec35 = minute_response['data'][34]['precip']

    ts36 = minute_response['data'][35]['ts']
    time36 = datetime.fromtimestamp(ts36).time()
    date36 = datetime.fromtimestamp(ts36).date()
    prec36 = minute_response['data'][35]['precip']

    ts37 = minute_response['data'][36]['ts']
    time37 = datetime.fromtimestamp(ts37).time()
    date37 = datetime.fromtimestamp(ts37).date()
    prec37 = minute_response['data'][36]['precip']

    ts38 = minute_response['data'][37]['ts']
    time38 = datetime.fromtimestamp(ts38).time()
    date38 = datetime.fromtimestamp(ts38).date()
    prec38 = minute_response['data'][37]['precip']

    ts39 = minute_response['data'][38]['ts']
    time39 = datetime.fromtimestamp(ts39).time()
    date39 = datetime.fromtimestamp(ts39).date()
    prec39 = minute_response['data'][38]['precip']

    ts40 = minute_response['data'][39]['ts']
    time40 = datetime.fromtimestamp(ts40).time()
    date40 = datetime.fromtimestamp(ts40).date()
    prec40 = minute_response['data'][39]['precip']

    ts41 = minute_response['data'][40]['ts']
    time41 = datetime.fromtimestamp(ts41).time()
    date41 = datetime.fromtimestamp(ts41).date()
    prec41 = minute_response['data'][40]['precip']

    ts42 = minute_response['data'][41]['ts']
    time42 = datetime.fromtimestamp(ts42).time()
    date42 = datetime.fromtimestamp(ts42).date()
    prec42 = minute_response['data'][41]['precip']

    ts43 = minute_response['data'][42]['ts']
    time43 = datetime.fromtimestamp(ts43).time()
    date43 = datetime.fromtimestamp(ts43).date()
    prec43 = minute_response['data'][42]['precip']

    ts44 = minute_response['data'][43]['ts']
    time44 = datetime.fromtimestamp(ts44).time()
    date44 = datetime.fromtimestamp(ts44).date()
    prec44 = minute_response['data'][43]['precip']

    ts45 = minute_response['data'][44]['ts']
    time45 = datetime.fromtimestamp(ts45).time()
    date45 = datetime.fromtimestamp(ts45).date()
    prec45 = minute_response['data'][44]['precip']

    ts46 = minute_response['data'][45]['ts']
    time46 = datetime.fromtimestamp(ts46).time()
    date46 = datetime.fromtimestamp(ts46).date()
    prec46 = minute_response['data'][45]['precip']

    ts47 = minute_response['data'][46]['ts']
    time47 = datetime.fromtimestamp(ts47).time()
    date47 = datetime.fromtimestamp(ts47).date()
    prec47 = minute_response['data'][46]['precip']

    ts48 = minute_response['data'][47]['ts']
    time48 = datetime.fromtimestamp(ts48).time()
    date48 = datetime.fromtimestamp(ts48).date()
    prec48 = minute_response['data'][47]['precip']

    ts49 = minute_response['data'][48]['ts']
    time49 = datetime.fromtimestamp(ts49).time()
    date49 = datetime.fromtimestamp(ts49).date()
    prec49 = minute_response['data'][48]['precip']

    ts50 = minute_response['data'][49]['ts']
    time50 = datetime.fromtimestamp(ts50).time()
    date50 = datetime.fromtimestamp(ts50).date()
    prec50 = minute_response['data'][49]['precip']

    ts51 = minute_response['data'][50]['ts']
    time51 = datetime.fromtimestamp(ts51).time()
    date51 = datetime.fromtimestamp(ts51).date()
    prec51 = minute_response['data'][50]['precip']

    ts52 = minute_response['data'][51]['ts']
    time52 = datetime.fromtimestamp(ts52).time()
    date52 = datetime.fromtimestamp(ts52).date()
    prec52 = minute_response['data'][51]['precip']

    ts53 = minute_response['data'][52]['ts']
    time53 = datetime.fromtimestamp(ts53).time()
    date53 = datetime.fromtimestamp(ts53).date()
    prec53 = minute_response['data'][52]['precip']

    ts54 = minute_response['data'][53]['ts']
    time54 = datetime.fromtimestamp(ts54).time()
    date54 = datetime.fromtimestamp(ts54).date()
    prec54 = minute_response['data'][53]['precip']

    ts55 = minute_response['data'][54]['ts']
    time55 = datetime.fromtimestamp(ts55).time()
    date55 = datetime.fromtimestamp(ts55).date()
    prec55 = minute_response['data'][54]['precip']

    ts56 = minute_response['data'][55]['ts']
    time56 = datetime.fromtimestamp(ts56).time()
    date56 = datetime.fromtimestamp(ts56).date()
    prec56 = minute_response['data'][55]['precip']

    ts57 = minute_response['data'][56]['ts']
    time57 = datetime.fromtimestamp(ts57).time()
    date57 = datetime.fromtimestamp(ts57).date()
    prec57 = minute_response['data'][56]['precip']

    ts58 = minute_response['data'][57]['ts']
    time58 = datetime.fromtimestamp(ts58).time()
    date58 = datetime.fromtimestamp(ts58).date()
    prec58 = minute_response['data'][57]['precip']

    ts59 = minute_response['data'][58]['ts']
    time59 = datetime.fromtimestamp(ts59).time()
    date59 = datetime.fromtimestamp(ts59).date()
    prec59 = minute_response['data'][58]['precip']

    ts60 = minute_response['data'][59]['ts']
    time60 = datetime.fromtimestamp(ts60).time()
    date60 = datetime.fromtimestamp(ts60).date()
    prec60 = minute_response['data'][59]['precip']

    return render(request, 'init_app/minutecast.html', {'time1': time1, 'date1': date1, 'prec1': prec1,
                                                        'time2': time2, 'date2': date2, 'prec2': prec2,
                                                        'time3': time3, 'date3': date3, 'prec3': prec3,
                                                        'time4': time4, 'date4': date4, 'prec4': prec4,
                                                        'time5': time5, 'date5': date5, 'prec5': prec5,
                                                        'time6': time6, 'date6': date6, 'prec6': prec6,
                                                        'time7': time7, 'date7': date7, 'prec7': prec7,
                                                        'time8': time8, 'date8': date8, 'prec8': prec8,
                                                        'time9': time9, 'date9': date9, 'prec9': prec9,
                                                        'time10': time10, 'date10': date10, 'prec10': prec10,
                                                        'time11': time11, 'date11': date11, 'prec11': prec11,
                                                        'time12': time12, 'date12': date12, 'prec12': prec12,
                                                        'time13': time13, 'date13': date13, 'prec13': prec13,
                                                        'time14': time14, 'date14': date14, 'prec14': prec14,
                                                        'time15': time15, 'date15': date15, 'prec15': prec15,
                                                        'time16': time16, 'date16': date16, 'prec16': prec16,
                                                        'time17': time17, 'date17': date17, 'prec17': prec17,
                                                        'time18': time18, 'date18': date18, 'prec18': prec18,
                                                        'time19': time19, 'date19': date19, 'prec19': prec19,
                                                        'time20': time20, 'date20': date20, 'prec20': prec20,
                                                        'time21': time21, 'date21': date21, 'prec21': prec21,
                                                        'time22': time22, 'date22': date22, 'prec22': prec22,
                                                        'time23': time23, 'date23': date23, 'prec23': prec23,
                                                        'time24': time24, 'date24': date24, 'prec24': prec24,
                                                        'time25': time25, 'date25': date25, 'prec25': prec25,
                                                        'time26': time26, 'date26': date26, 'prec26': prec26,
                                                        'time27': time27, 'date27': date27, 'prec27': prec27,
                                                        'time28': time28, 'date28': date28, 'prec28': prec28,
                                                        'time29': time29, 'date29': date29, 'prec29': prec29,
                                                        'time30': time30, 'date30': date30, 'prec30': prec30,
                                                        'time31': time31, 'date31': date31, 'prec31': prec31,
                                                        'time32': time32, 'date32': date32, 'prec32': prec32,
                                                        'time33': time33, 'date33': date33, 'prec33': prec33,
                                                        'time34': time34, 'date34': date34, 'prec34': prec34,
                                                        'time35': time35, 'date35': date35, 'prec35': prec35,
                                                        'time36': time36, 'date36': date36, 'prec36': prec36,
                                                        'time37': time37, 'date37': date37, 'prec37': prec37,
                                                        'time38': time38, 'date38': date38, 'prec38': prec38,
                                                        'time39': time39, 'date39': date39, 'prec39': prec39,
                                                        'time40': time40, 'date40': date40, 'prec40': prec40,
                                                        'time41': time41, 'date41': date41, 'prec41': prec41,
                                                        'time42': time42, 'date42': date42, 'prec42': prec42,
                                                        'time43': time43, 'date43': date43, 'prec43': prec43,
                                                        'time44': time44, 'date44': date44, 'prec44': prec44,
                                                        'time45': time45, 'date45': date45, 'prec45': prec45,
                                                        'time46': time46, 'date46': date46, 'prec46': prec46,
                                                        'time47': time47, 'date47': date47, 'prec47': prec47,
                                                        'time48': time48, 'date48': date48, 'prec48': prec48,
                                                        'time49': time49, 'date49': date49, 'prec49': prec49,
                                                        'time50': time50, 'date50': date50, 'prec50': prec50,
                                                        'time51': time51, 'date51': date51, 'prec51': prec51,
                                                        'time52': time52, 'date52': date52, 'prec52': prec52,
                                                        'time53': time53, 'date53': date53, 'prec53': prec53,
                                                        'time54': time54, 'date54': date54, 'prec54': prec54,
                                                        'time55': time55, 'date55': date55, 'prec55': prec55,
                                                        'time56': time56, 'date56': date56, 'prec56': prec56,
                                                        'time57': time57, 'date57': date57, 'prec57': prec57,
                                                        'time58': time58, 'date58': date58, 'prec58': prec58,
                                                        'time59': time59, 'date59': date59, 'prec59': prec59,
                                                        'time60': time60, 'date60': date60, 'prec60': prec60})

def airPage(request):
    city = request.session['city_name']
    city_url = 'http://api.openweathermap.org/geo/1.0/direct'
    city_params = {
        'q': city,
        'appid': '06bd41884aaba0781ff1a2a6ee800b9a'
    }
    city_request = requests.get(url=city_url, params=city_params)
    city_response = city_request.json()
    latitude = city_response[0]['lat']
    longitude = city_response[0]['lon']
    lat = str(latitude)
    lon = str(longitude)

    air_url = 'http://api.openweathermap.org/data/2.5/air_pollution'
    air_params = {
        'lat': lat,
        'lon': lon,
        'appid': '06bd41884aaba0781ff1a2a6ee800b9a'
    }
    air_request = requests.get(url=air_url, params=air_params)
    air_response = air_request.json()
    aqi = air_response['list'][0]['main']['aqi']
    co = air_response['list'][0]['components']['co']
    no = air_response['list'][0]['components']['no']
    no2 = air_response['list'][0]['components']['no2']
    o3 = air_response['list'][0]['components']['o3']
    so2 = air_response['list'][0]['components']['so2']
    pm2_5 = air_response['list'][0]['components']['pm2_5']
    pm10 = air_response['list'][0]['components']['pm10']
    nh3 = air_response['list'][0]['components']['nh3']

    return render(request, 'init_app/air_quality.html', {'aqi': aqi,
                                                         'co': co,
                                                         'no': no,
                                                         'no2': no2,
                                                         'o3': o3,
                                                         'so2': so2,
                                                         'pm2_5': pm2_5,
                                                         'pm10': pm10,
                                                         'nh3': nh3})