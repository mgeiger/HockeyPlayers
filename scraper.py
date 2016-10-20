# import csv
# from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
from geopy.geocoders import Nominatim, Photon
from geopy.exc import GeocoderTimedOut
import os
import pickle
import matplotlib.pyplot as plt
import time
# from mpl_toolkits.basemap import Basemap

base_url = 'http://www.hockey-reference.com'
base_year_url = '{}/leagues/NHL_{}_skaters.html'
min_year = 1918
max_year = 2016
years = range(min_year, max_year, 1)
geolocator = Nominatim()

average_latitude = [None] * len(years)
average_longitude = [None] * len(years)


def get_location(skater):
    data = requests.get(skater.url)
    soup = BeautifulSoup(data.content, 'html.parser')
    # Look for id="info_box"
    background = soup.find(id='info_box').findAll('p', {'class': 'clear_left'})[0]
    home = background.get_text().split('\n')[0].split(' in ')[1].strip()
    try:
        location = geolocator.geocode(home)
        if not location:
            print('Could not find location for {} ({}).\nAttempting to use Photon service.'.format(skater, home))
            gp = Photon()
            location = gp.geocode(home)
            if not location:
                raise Exception('Failure to find location for {}.'.format(skater))
    except GeocoderTimedOut:
        print('Timed out trying to find {}. Waiting 5 seconds.'.format(skater))
        time.sleep(5)
        home = home.replace('Union of Soviet Socialist Republics', 'Russia')
        location = geolocator.geocode(home)
        if not location:
            print('After timeout, could not find location for {}.\nAttempting to use Photon service.'.format(skater))
            gp = Photon()
            location = gp.geocode(home)
    return location

if __name__ == "__main__":
    for i, year in enumerate(years):
        print('\nWorking on {}.'.format(year))
        year_url = base_year_url.format(base_url, year)
        print(year_url)
        data = requests.get(year_url)
        soup = BeautifulSoup(data.content, 'html.parser')
        try:
            rows_stats = soup.find(id='stats').findChildren(['tr'])
        except AttributeError:
            print('{}: The Strike Year.'.format(year))

        skaters = 0
        total_games = 0
        total_latitude = 0
        total_longitude = 0

        for row_stats in rows_stats:
            try:
                # Parse our the information we need
                item = row_stats.findAll('td')[1]
                # Find the number of games this player appeared in
                player_games = int(row_stats.findAll('td')[5].getText())
                total_games += player_games
                player_name = item.getText().replace('*', '')
                player_root = item.find_all('a', href=True)[0]['href']
                pickle_path = '.' + os.path.splitext(player_root)[0]
                if os.path.exists(pickle_path):
                    with open(pickle_path, 'rb') as pickle_file:
                        skater = pickle.load(pickle_file)
                    if not skater.location:
                        skater.location = get_location(skater)
                        with open(pickle_path, 'wb') as pickle_file:
                            pickle.dump(skater, pickle_file)
                else:
                    player_link = base_url + player_root
                    # Generate a new skater
                    skater = Skater(player_name, player_link)
                    try:
                        skater.location = get_location(skater)
                        pickle_dir = os.path.dirname(pickle_path)
                        if not os.path.isdir(pickle_dir):
                            os.makedirs(pickle_dir)
                        with open(pickle_path, 'wb') as pickle_file:
                            pickle.dump(skater, pickle_file)
                    except GeocoderTimedOut:
                        print('Skipping {} as they are having a problem getting their location.'.format(skater))

                if skater.location:
                    # Total numbers
                    total_latitude += skater.location.latitude
                    total_longitude += skater.location.longitude
                    # print(skater)
                    # print(skater.get_home())
                    # Increment Total Number of Skaters for this season
                    skaters += 1
            except IndexError:
                print('Found an Index Error. Skipping.')
                pass

        average_latitude[i] = total_latitude / skaters
        average_longitude[i] = total_longitude / skaters

        print('Found {} skaters who played an average of {:.2f} games for {}.'.format(skaters, total_games/skaters, year))
        print('Their average location is ({}, {}).'.format(average_latitude[i], average_longitude[i]))

    # plt.scatter(average_longitude, average_latitude)
    plt.plot(average_longitude, average_latitude)
    plt.show()
