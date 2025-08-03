# WeatherApp: Real-time Weather with Location Detection
# Requirements: requests, geocoder, tkinter

import tkinter as tk
from tkinter import messagebox
import requests
import geocoder

# You need to get a free API key from https://openweathermap.org/api
API_KEY = 'd0bf3784701b405bae55bb19d5627926'  # User's actual API key

# Function to get user's location (city)
def get_location():
    g = geocoder.ip('me')
    if g.ok:
        return g.city
    return None

# Function to get weather data for a city
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    try:
        return response.json()
    except Exception:
        return {"message": "Invalid response from server."}

# Function to update weather info in the GUI
def update_weather():
    city = city_var.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name.")
        return
    data = get_weather(city)
    if data:
        try:
            weather = data['weather'][0]['description'].title()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind = data['wind']['speed']
            result = f"Weather: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%\nWind Speed: {wind} m/s"
            result_label.config(text=result)
        except Exception as e:
            # If the expected fields are missing, show the raw API message
            error_message = data.get('message', str(e))
            result_label.config(text=f"Error: {error_message}")
    else:
        result_label.config(text="Could not retrieve weather data. (No response)")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("350x250")
root.resizable(False, False)

city_var = tk.StringVar()

# Try to auto-detect location
auto_city = get_location()
if auto_city:
    city_var.set(auto_city)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True)

city_label = tk.Label(frame, text="City:")
city_label.grid(row=0, column=0, sticky='w')
city_entry = tk.Entry(frame, textvariable=city_var, width=25)
city_entry.grid(row=0, column=1, padx=5)

get_btn = tk.Button(frame, text="Get Weather", command=update_weather)
get_btn.grid(row=0, column=2, padx=5)

result_label = tk.Label(frame, text="", justify='left', font=("Arial", 11), pady=20)
result_label.grid(row=1, column=0, columnspan=3)

root.mainloop()
