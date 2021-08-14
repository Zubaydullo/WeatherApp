import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm
from datetime import date, datetime

def home(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e5472bae81702f27e4dccddba51928ab'
	if request.method == 'POST':
		form = CityForm(request.POST)
		form.save()

	form = CityForm()
	cities = City.objects.all()

	weather_data = []

	for city in cities:
		r = requests.get(url.format(city)).json()
		# print(r.text)

		city_weather = {
			'city': city.name,
			# 'temperature': r['main']['temp'],
			'description': r['weather'][0]['description'],
			'icon': r['weather'][0]['icon'],
		}


		weather_data.append(city_weather)
	weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
	today = date.today()
	now = datetime.now()
	current_time = now.strftime("%H:%M")
	week_day_number = datetime.today().weekday()
	week_day = weekDays[week_day_number]

	context = {'weather_data': weather_data, 'form': form, 'today':today, 'current_time': current_time, 'week_day':week_day}
	return render(request, 'weather/weather.html', context)
