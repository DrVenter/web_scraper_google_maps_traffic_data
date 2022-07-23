import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import time
import random
import math
import datetime

print("Scraper Started")
folder_files = [
    r"C:\Users\vente\OneDrive\Documents\Code\web_scraper_google_maps\random_coordinates_from-26.207201909503596,28.04650823914504.txt", 
    r"C:\Users\vente\OneDrive\Documents\Code\web_scraper_google_maps\random_coordinates_from-29.6004500675832,30.378738192502244.txt"
    ]
database = pd.read_csv(r"C:\Users\vente\OneDrive\Documents\Code\web_scraper_google_maps\google_maps_traffic_data.csv")
data_columns = database.columns

for text_file in folder_files:
    file = open(text_file)
    file = file.read()
    file = file.split("\n")

    from_location = [file[0].replace("from:", "")]
    to_location = file[1:]

    root_URL = "https://www.google.com/maps/dir/"

    for number in range(2):
        for from_loc in from_location:
            for to_loc in to_location:
                URL = root_URL + from_loc + "/" + to_loc
                page = requests.get(URL) 
                soup = BeautifulSoup(page.content, "html.parser") 
                date_time = datetime.datetime.now()
                date = date_time.strftime("%Y-%m-%d")
                hour = date_time.strftime("%H")

                soup = str(soup)
                if "Our systems have detected unusual traffic from your computer network." in soup:
                    print("Scraper Blocked")
                    break

                distance = soup.find(' km') #the whole script relies on finding this
                section = np.array(soup[distance - 200: distance+400].split('\\"'))

                unwanted_characters = list("[]/\\_:")
                for character in unwanted_characters: section = section[np.char.find(section, character) == -1]
                unwanted_list_items = list(", ")
                for item in unwanted_characters: section = section[section != ","]

                try:
                    distance  = section[np.char.find(section, "km") != -1][0]
                    time_no_traffic = section[np.where(section == distance)[0] + 1][0]
                    time_traffic = section[np.where(section == distance)[0] + 2][0]
                    time_range = section[np.char.find(section, " - ") != -1][0]
                    row = [date, hour, from_loc, to_loc, distance, time_no_traffic, time_traffic, time_range]
                except:
                    row = [date, hour, from_loc, to_loc, None, None, None, None]
                
                row_data = pd.DataFrame([row], columns=data_columns)
                database = pd.concat([database, row_data])

                print("Completed: ", row)
                wait_time_seconds = random.randrange(5, 10)
                time.sleep(wait_time_seconds)
        from_location, to_location = to_location, from_location
    if "Our systems have detected unusual traffic from your computer network." in soup:
        print("Scraper Blocked")
        
        break
    print("Completed: Text File")

database.to_csv(r"C:\Users\vente\OneDrive\Documents\Code\web_scraper_google_maps\google_maps_traffic_data.csv", index=False)
print("Scaper Finished")