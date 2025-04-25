from flask import Flask, render_template, request, flash
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

WEATHER_API_KEY = "3a56e9d06c844614b0265438241102"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_info = {}
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                # Current weather information request
                url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
                response = requests.get(url)
                current_data = response.json()

                # Astronomy information request
                url_ast = f"https://api.weatherapi.com/v1/astronomy.json?key={WEATHER_API_KEY}&q={city}"
                response_ast = requests.get(url_ast)
                astro_data = response_ast.json()

                # Extract sunrise and sunset times from API (format e.g., "07:05 AM")
                sunrise_str = astro_data['astronomy']['astro']['sunrise']
                sunset_str = astro_data['astronomy']['astro']['sunset']

                # Compute day length by parsing times into datetime objects.
                time_format = "%I:%M %p"  # Format for "07:05 AM" style times
                sunrise_time = datetime.strptime(sunrise_str, time_format)
                sunset_time = datetime.strptime(sunset_str, time_format)
                # Calculate the difference; assumes both are on the same day.
                day_length = sunset_time - sunrise_time

                # Merge data into a single dictionary for ease of use in the template
                weather_info = {
                    "name": current_data['location']['name'],
                    "region": current_data['location']['region'],
                    "country": current_data['location']['country'],
                    "tz_id": current_data['location']['tz_id'],
                    "localtime": current_data['location']['localtime'],
                    "temp_c": current_data['current']['temp_c'],
                    "last_updated": current_data['current']['last_updated'],
                    "condition": current_data['current']['condition']['text'],
                    "wind_kph": current_data['current']['wind_kph'],
                    "wind_degree": current_data['current']['wind_degree'],
                    "precip_mm": current_data['current']['precip_mm'],
                    "pressure_in": current_data['current']['pressure_in'],
                    "humidity": current_data['current']['humidity'],
                    "cloud": current_data['current']['cloud'],
                    "feelslike_c": current_data['current']['feelslike_c'],
                    "vis_km": current_data['current']['vis_km'],
                    "uv": current_data['current']['uv'],
                    "sunrise": sunrise_str,
                    "sunset": sunset_str,
                    "moonrise": astro_data['astronomy']['astro']['moonrise'],
                    "moonset": astro_data['astronomy']['astro']['moonset'],
                    "moon_phase": astro_data['astronomy']['astro']['moon_phase'],
                    "moon_illumination": astro_data['astronomy']['astro']['moon_illumination'],
                    "day_length": str(day_length)  # Display as HH:MM:SS
                }
            except Exception as e:
                flash("Error retrieving weather information. Please check the city name and try again.")
    return render_template("index.html", weather=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
