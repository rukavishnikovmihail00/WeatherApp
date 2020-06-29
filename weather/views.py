from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    appid = '47c065c2228f4a548bca5be0928f933f'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    

    if(request.method == 'POST'):
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    all_cities = []
    check = False

    for city in cities: 
        res = requests.get(url.format(city.name)).json() # конвертирует json формат в словари
        lat = res["coord"]["lat"]
        lon = res["coord"]["lon"]
        url_hourly = 'https://api.openweathermap.org/data/2.5/onecall?lat=' + str(lat) + '&lon=' + str(lon)  + '&exclude=daily&appid=' + appid
        res_hourly = requests.get(url_hourly).json()
        #if (city.name == 'Moscow'):
            #print(res_hourly)
        try:
            city_info = {
                'city': city.name,
                'temp': res["main"]["temp"],
                'icon': res["weather"][0]["icon"],
                'desc': res["weather"][0]["description"],
                'feel': res["main"]["feels_like"],
               # 'min': res_hourly["daily"][0]["min"],
               # 'max': res_hourly["daily"][0]["max"],
            }

            
            all_cities.append(city_info)
        except KeyError:
            check = True

    

    context = {'all_info':all_cities, 'form':form}
    
    return render(request, 'weather/index.html' , context)

def info(request):
    return render(request, 'weather/info.html')


def contacts(request):
    return render(request, 'weather/contacts.html')

def weather_full(request):
    return render(request, 'weather/weather_full.html')