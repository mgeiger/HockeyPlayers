

# This Class will be used to generate a skater.
# We will eventually have a list of skaters that can be pickled
# We really want a database
class Skater:
    name = None
    url = None
    location = None

    def __init__(self, name, url, location=None):
        self.name = name
        self.url = url
        self.location = location

    # def update_location(self):
    #     data = requests.get(self.url)
    #     soup = BeautifulSoup(data.content, 'html.parser')
    #     # Look for id="info_box"
    #     background = soup.find(id='info_box').findAll('p', {'class': 'clear_left'})[0]
    #     home = background.get_text().split('\n')[0].split(' in ')[1].strip()
    #     self.location = geolocator.geocode(home)
    #     if not self.location:
    #         gp = Photon()
    #         self.location = gp.geocode(home)
    #     print('Found ({:.2f}, {:.2f}) for {}.'.format(self.location.latitude, self.location.longitude, self.name))

    def get_location(self):
        # if not self.location:
        #     self.location = get_location(self)
        return self.location

    def __str__(self):
        # if not self.location:
        #     self.location = get_location(self)
        return "{}".format(self.name)
        return "{{{}: {{'location': ({}, {})}}}}".format(self.name, self.location.latitude, self.location.longitude)

