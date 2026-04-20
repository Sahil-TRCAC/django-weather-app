import requests
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages

def home(request):
    """Render the home page with weather form"""
    return render(request, 'weather_app/home.html')

def get_weather(request):
    """Fetch weather data from Weatherstack API"""
    if request.method == 'POST':
        location = request.POST.get('location')
        
        if not location:
            messages.error(request, 'Please enter a location')
            return render(request, 'weather_app/home.html')
        
        # Weatherstack API endpoint
        api_url = 'http://api.weatherstack.com/current'
        
        # API parameters
        params = {
            'access_key': settings.WEATHERSTACK_API_KEY,
            'query': location,
            'units': 'm'  # m for Celsius, f for Fahrenheit
        }
        
        try:
            # Make API request
            response = requests.get(api_url, params=params)
            data = response.json()
            
            # Check if API request was successful
            if response.status_code == 200:
                if 'error' in data:
                    messages.error(request, f"Error: {data['error']['info']}")
                    return render(request, 'weather_app/home.html')
                
                # Extract weather data
                weather_data = {
                    'location': data['location']['name'],
                    'country': data['location']['country'],
                    'temperature': data['current']['temperature'],
                    'feels_like': data['current']['feelslike'],
                    'weather_description': data['current']['weather_descriptions'][0],
                    'weather_icon': data['current']['weather_icons'][0],
                    'humidity': data['current']['humidity'],
                    'wind_speed': data['current']['wind_speed'],
                    'wind_dir': data['current']['wind_dir'],
                    'pressure': data['current']['pressure'],
                    'precip': data['current']['precip'],
                    'uv_index': data['current']['uv_index'],
                    'visibility': data['current']['visibility'],
                    'observation_time': data['current']['observation_time'],
                }
                
                return render(request, 'weather_app/weather_result.html', {'weather': weather_data})
            else:
                messages.error(request, 'Failed to fetch weather data. Please try again.')
                return render(request, 'weather_app/home.html')
                
        except requests.exceptions.RequestException as e:
            messages.error(request, f'Network error: {str(e)}')
            return render(request, 'weather_app/home.html')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'weather_app/home.html')
    
    return render(request, 'weather_app/home.html')