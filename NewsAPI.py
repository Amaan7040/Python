import requests
import json

search = input("Enter the tyore of new you want :: ")
url = f"https://newsapi.org/v2/top-headlines?country=us&{search}category=business&apiKey=1b4706677b2c4e0996b86c3eee2389c1"
response = requests.get(url)
if(response.status_code==200):
    print(f"Status Code :: {response.status_code} and type :: {type(response.status_code)}.")
    print("Connection is established successfuly.")
news = json.loads(response.text)
for article in news["articles"]:
    print("Title\n",article["title"])
    print("\nDescription\n",article["description"])
    print("----------------------------------------------------------------------------------------------------------------------------")
