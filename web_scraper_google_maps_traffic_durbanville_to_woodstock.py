import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import time
import random
import math
import datetime

print("Scraper Started")
database = pd.read_csv(r"C:\Users\vente\OneDrive\Documents\Code\web_scraper_google_maps\google_maps_traffic_data_durbaville_to_woodstock.csv")
data_columns = database.columns

from_location = ["-33.81507725499659,18.671698314355297"]
to_location = ["-33.926444610865296,18.445965448645833"]

root_URL = "https://www.google.com/maps/dir/"

for number in range(2):
    for from_loc in from_location:
        for to_loc in to_location:
            URL = root_URL + from_loc + "/" + to_loc
            page = requests.get(URL) 
            soup = BeautifulSoup(page.content, "html.parser") 
            date_time = datetime.datetime.now()
            date = date_time.strftime("%Y-%m-%d")
            hour = date_time.strftime("%H-%M")

            soup = str(soup)
            if "Our systems have detected unusual traffic from your computer network." in soup:
                print("Scraper Blocked")
                break          
    
            distance = soup.find(' km') #the whole script relies on finding this
            if distance != -1:
                section = np.array(soup[distance - 200: distance+1200].split('\\"'))

                unwanted_characters = list("[]/\\_:")
                for character in unwanted_characters: section = section[np.char.find(section, character) == -1]
                unwanted_list_items = list(", ")
                for item in unwanted_list_items: section = section[section != ","]
                section = section[(np.char.find(section, " km") != -1) | (np.char.find(section, " min") != -1) | (np.char.find(section, " hr") != -1)]

                try:
                    distance  = section[np.char.find(section, "km") != -1][0]
                    time_no_traffic = section[np.where(section == distance)[0] + 1][0]
                    time_traffic = section[np.where(section == distance)[0] + 2][0]
                    time_range = section[np.char.find(section, " - ") != -1][0]
                except:
                    distance, time_no_traffic, time_traffic, time_range = None, None, None, None 
                
                row = [date, hour, from_loc, to_loc, distance, time_no_traffic, time_traffic, time_range]

                row_data = pd.DataFrame([row], columns=data_columns)
                database = pd.concat([database, row_data])
            else:
                print("Could not find distance. Skipping.")
                continue
                
            print("Completed: ", row)
            wait_time_seconds = random.randrange(5, 10)
            time.sleep(wait_time_seconds)
            
    from_location, to_location = to_location, from_location

database.to_csv(r"C:\Users\vente\OneDrive\Documents\Code\web_scraper_google_maps\google_maps_traffic_data_durbaville_to_woodstock.csv", index=False)
print("Scaper Finished")