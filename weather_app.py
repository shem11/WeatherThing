import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        complete_api_link = requests.get(f"https://api.openweathermap.org/data/2.5/weather?zip={zip_code},us&appid=51a01a1a70bc47e2f23fc0e9740d3699")
        objects = complete_api_link.json()

        precipitation = str(objects['weather'][0]['main'])
        wind_speed = float(objects['wind']['speed'])
        temperatureK = float(objects['main']['temp'])
        temperatureF = int(round(((temperatureK - 273.15) * (9/5)) + 32))
        windmph = int(round(wind_speed * 2.237))
        humidity = int(objects['main']['humidity'])
        

        def Make_Decision(precipitation, windmph, temperatureF, humidity):
            outerwear = ''
            top = ''
            bottoms = ''
            shoes = ''
            #No Precipitation
            if precipitation == 'Clear':
                if temperatureF < 55:
                    outerwear = "Coat or Sweater"
                    bottoms = 'Pants'
                    top = 'Long sleeve Shirt'
                    shoes = 'Only-closed Toed shoes'
                if 55 <= temperatureF <= 75:
                    bottoms = 'Any Bottoms'
                    shoes = 'Sneakers'
                    if windmph <= 7:
                        outerwear = 'Jacket or Light Sweater'
                        top = 'T-shirt'
                    else:
                        outerwear = 'Windbreaker'
                        top = 'Long sleeve Shirt'
                if temperatureF > 75:
                    outerwear = "No Outerwear"
                    shoes = 'Sneakers or Sandals'
                    bottoms = 'Shorts or Skirt'
                    if humidity > 70:
                        top = "T-shirt only"
                    else:
                        top = 'Any Top'

            #Drizzle

            if precipitation == 'Drizzle':
                shoes = 'Only-closed Toed shoes'
                if temperatureF < 55:
                    top = 'Long sleeve Shirt'
                    outerwear = 'Coat or Hoodie'
                    bottom = 'Pants'
                if 55 <= temperatureF <= 75:
                    top = 'Any Top'
                    if windmph > 7:
                        outerwear = 'Windbreaker'
                    else:
                        outerwear = 'Jacket or Hoodie'
                if temperatureF > 75:
                    outerwear = "Jacket"
                    shoes = 'Sneakers'
                    bottoms = 'Shorts or Skirt'
                    if humidity > 70:
                        top = "T-shirt only"
                    else:
                        top = 'Any Top'

            #Rain

            if precipitation == 'Rain':
                shoes = 'Only-closed Toed shoes'
                if temperatureF < 55:
                    top = 'Long sleeve Shirt'
                    outerwear = 'Coat or Rain Jacket with Sweater'
                    bottom = 'Pants'
                if 55 <= temperatureF <= 75:
                    top = 'Any Top'
                    if windmph > 7:
                        outerwear = 'Rain Jacket'
                        bottoms = 'Pants'
                    else:
                        outerwear = 'Jacket or Hoodie'
                        bottoms = 'Any Bottoms'
                if temperatureF > 75:
                    outerwear = "Jacket"
                    shoes = 'Sneakers'
                    bottoms = 'Shorts or Skirt'
                    if humidity > 70:
                        top = "T-shirt only"
                    else:
                        top = 'Any Top'

            #Thunderstorm

            if precipitation == 'Thunderstorm':
                shoes = 'Only-closed Toed shoes'
                bottoms = 'Pants'
                if temperatureF < 55:
                    top = 'Long sleeve Shirt'
                    outerwear = 'Coat or Rain Jacket with Sweater'
                if 55 <= temperatureF <= 75:
                    top = 'Any Top'
                    if windmph > 7:
                        outerwear = 'Rain Jacket'
                    else:
                        outerwear = 'Jacket or Hoodie'
                if temperatureF > 75:
                    outerwear = "Jacket"
                    shoes = 'Sneakers'
                    if humidity > 70:
                        top = "T-shirt only"
                    else:
                        top = 'Any Top'

            #Snow

            if precipitation == 'Snow':
                bottoms = 'Pants'
                shoes = 'Only-closed Toed shoes'
                top = 'Long sleeve Shirt'
                if temperatureF < 32:
                    outerwear = 'Coat'
                else:
                    outerwear = 'Coat or a Hoodie'

            #Cloudy

            if precipitation == 'Clouds':
                if temperatureF < 55:
                    outerwear = "Coat or Sweater"
                    bottoms = 'Pants'
                    top = 'Long sleeve Shirt'
                    shoes = 'Only-closed Toed shoes'
                if 55 <= temperatureF <= 75:
                    bottoms = 'Any Bottoms'
                    shoes = 'Sneakers'
                    if windmph <= 7:
                        outerwear = 'Jacket or Light Sweater'
                        top = 'T-shirt'
                    else:
                        outerwear = 'Windbreaker or Jacket'
                        top = 'Long sleeve Shirt or Sweater with no Outerwear'
                if temperatureF > 75:
                    outerwear = "None"
                    shoes = 'Sneakers or Sandals'
                    bottoms = 'Shorts or Skirt'
                    if humidity > 70:
                        top = "T-shirt only"
                    else:
                        top = 'Any Top'

            return {"Weather Details": f'Weather conditions in your location: {precipitation}, {temperatureF} degrees, {windmph} mph wind, and {humidity}% humidity',
                    "Outerwear": outerwear, 
                    "Top": top, 
                    "Bottoms":bottoms,
                    "Shoes": shoes}
            
        recommendations = Make_Decision(precipitation, windmph, temperatureF, humidity)
        return render_template('result.html', recommendations=recommendations)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()