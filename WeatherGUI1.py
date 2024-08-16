import json
import requests
import tkinter as tk
from tkinter import messagebox
import win32com.client as w

class WEATHER:

  def __init__(self):
      self.root = tk.Tk()
      self.root.geometry("1500x1500")
      self.root.title("Weather App")
      self.label = tk.Label(self.root,fg="Blue",text="WELCOME TO KNOW WEATHER",font=("ARIAL",24),borderwidth=5)
      self.label.grid(row=0, column= 300)
      self.l = tk.Label(self.root, text="Enter City:",font=("Arial",16))
      self.l.grid(row=2, column=100)
      self.entry = tk.Entry(borderwidth=3,fg="Green",bg="white",font=("Arial",16))
      self.entry.grid(row=2, column=101)
      self.btn = tk.Button(self.root,text="Search Weather",fg="White",bg="Black",font=("arial",16),borderwidth=4,command=self.api)
      self.btn.grid(row=3, column=100, columnspan=2, pady=40)
      self.text = tk.Text(self.root,height=15,width=70,fg="Blue",bg="green",font=("Arial",18),borderwidth=10,cursor="hand2")
      self.text.grid(row=5,column = 300)
      self.btn = tk.Button(self.root,text="CLEAR",fg="White",bg="Blue",font=("arial",16),borderwidth=4,command=self.ask)
      self.btn.grid(column = 300)
      self.root.protocol("WM_DELETE_WINDOW",self.close)
      self.root.mainloop()

  def a(self):
      self.city = self.entry.get()

  def close(self):
      if messagebox.askyesno(title="Quit?",message="Do you want to quit this window?"):
          self.root.destroy()

  def ask(self):
      if messagebox.askyesno(title="Clear?",message="Do you want to clear the text"):
         messagebox.showwarning(title="Warning...", message="Text will be cleared.")
         self.text.delete(1.0, tk.END)  # Clears previous content

  def api(self):
      self.a()
      speaker = w.Dispatch("SAPI.SpVoice")
      self.url = f"https://api.weatherapi.com/v1/current.json?key=3a56e9d06c844614b0265438241102&q={self.city}"
      self.r = requests.get(self.url)
      self.wdic = json.loads(self.r.text)

      self.url1 = f"https://api.weatherapi.com/v1/astronomy.json?key=3a56e9d06c844614b0265438241102&q={self.city}"
      self.r1 = requests.get(self.url1)
      self.wd = json.loads(self.r1.text)

      self.entry.delete(0,tk.END)

      self.text.insert(tk.END, f"Name: {self.wdic['location']['name']}\n")
      self.text.insert(tk.END, f"Region: {self.wdic['location']['region']}\n")
      self.text.insert(tk.END, f"Country: {self.wdic['location']['country']}\n")
      self.text.insert(tk.END, f"Continent: {self.wdic['location']['tz_id']}\n")
      self.text.insert(tk.END, f"LocalTime: {self.wdic['location']['localtime']}\n")
      self.text.insert(tk.END, f"Current temperature: {self.wdic['current']['temp_c']}°C\n")
      self.text.insert(tk.END, f"Last Updated: {self.wdic['current']['last_updated']}\n")
      self.text.insert(tk.END, f"Weather: {self.wdic['current']['condition']['text']}\n")
      self.text.insert(tk.END, f"Wind Speed: {self.wdic['current']['wind_kph']} km/h\n")
      self.text.insert(tk.END, f"Wind Degree: {self.wdic['current']['wind_degree']}\n")
      self.text.insert(tk.END, f"Precipitation (in mm): {self.wdic['current']['precip_mm']}\n")
      self.text.insert(tk.END, f"Pressure (in inches): {self.wdic['current']['pressure_in']}\n")
      self.text.insert(tk.END, f"Humidity: {self.wdic['current']['humidity']}%\n")
      self.text.insert(tk.END, f"Clouds Percentage: {self.wdic['current']['cloud']}%\n")
      self.text.insert(tk.END, f"Feels Like: {self.wdic['current']['feelslike_c']}°C\n")
      self.text.insert(tk.END, f"Visibility: {self.wdic['current']['vis_km']} km\n")
      self.text.insert(tk.END, f"UV: {self.wdic['current']['uv']}\n\n")
      self.text.insert(tk.END, "Here are some astronomical information as well,\n")
      self.text.insert(tk.END, f"Sunrise: {self.wd['astronomy']['astro']['sunrise']}\n")
      self.text.insert(tk.END, f"Sunset: {self.wd['astronomy']['astro']['sunset']}\n")
      self.text.insert(tk.END, f"Moonrise: {self.wd['astronomy']['astro']['moonrise']}\n")
      self.text.insert(tk.END, f"Moonset: {self.wd['astronomy']['astro']['moonset']}\n")
      self.text.insert(tk.END, f"Moon's Phase: {self.wd['astronomy']['astro']['moon_phase']}\n")

      weather_info = f"Current weather in {self.wdic['location']['name']} is {self.wdic['current']['temp_c']}°C.However there are some other information which ypu can see in the screen"
      speaker.Speak(weather_info)
WEATHER()