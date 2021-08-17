import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from datetime import date, datetime
from django.contrib import messages
import pytz
tz = pytz.timezone('Europe/Berlin')
berlin_now = datetime.now(tz)

def check_city(city):
	cities = City.objects.all()
	city_names = []
	for city in cities:
		city_names.append(city.name)
	if city in city_names:
		return True
	else:
		return False


def home(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=e5472bae81702f27e4dccddba51928ab'

	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			form.save()
		else:
			messages.warning(request, "The city name exists in the website!")
			return redirect('home')


	form = CityForm()

	weather_data = []
	cities = City.objects.all()
	for city in cities:
		r = requests.get(url.format(city)).json()
		if not r['cod'] == '404':
			city_weather = {
				'city': city.name,
				'temperature': r['main']['temp'],
				'description': r['weather'][0]['description'],
				'icon': r['weather'][0]['icon'],
			}
			weather_data.append(city_weather)
		else:
			messages.warning(request, "Please enter the valid city name!")
			city.delete()
	weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
	today = date.today()
	now = datetime.now()
	current_time = now.strftime("%H:%M")
	week_day_number = datetime.today().weekday()
	week_day = weekDays[week_day_number]

	context = {'weather_data': weather_data,
			   'form': form, 'today':today,
			   'current_time': current_time, 'week_day':week_day}
	return render(request, 'weather/weather.html', context)


def remove_city(request, name):
	city = City.objects.get(name=name)
	city.delete()
	return redirect('home')
