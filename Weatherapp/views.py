from django.shortcuts import render
import requests
import datetime
from django.contrib import messages

def home(request):
    city = request.POST.get('city', 'Paris')

    # Weather API
    URL = "https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {
        'q': city,
        'appid': 'dc28f823ace6421a0d111299e94921c3',
        'units': 'metric'
    }

    # Google Custom Search API
    API_KEY = 'AIzaSyDjy5u-vGoLF6NrKpc2AyvVkjuUKoOlFmA'
    SEARCH_ENGINE_ID = '9718d137bbb5941ce'
    query = f"{city} 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'

    try:
        # Get image URL
        city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"
        img_data = requests.get(city_url).json()
        search_items = img_data.get("items", [])
        image_url = search_items[1]['link'] if len(search_items) > 1 else None

        # Get weather data
        weather_data = requests.get(URL, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'Weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url': image_url,
            'exception_occurred': False
        })

    except Exception as e:
        messages.error(request, 'Entered data is not available at API')
        day = datetime.date.today()
        return render(request, 'Weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'Paris',
            'image_url': None,
            'exception_occurred': True
        })
