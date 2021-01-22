import requests
from bs4 import BeautifulSoup
import json
import time
import csv

class ZillowScraper():
    results = []
    headers = { #headers to reach Zillow site
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'en-US,en;q=0.9',
        'Cache-Control' : 'max-age=0',
        'Connection' : 'keep-alive',
        'Cookie' : 'zguid=23|%24a6deaf10-1607-4349-b062-7ff3330d5d3f; _ga=GA1.2.1728922627.1608927046; zjs_user_id=null; zjs_anonymous_id=%22a6deaf10-1607-4349-b062-7ff3330d5d3f%22; _gcl_au=1.1.1099525802.1608927047; _pxvid=46b3994e-46ed-11eb-b369-0242ac12000b; _pin_unauth=dWlkPU1EQXhNR00wWVdJdFpERmpPQzAwWVdKa0xXSXdaamd0TW1GallUZ3pOekZoWW1NMA; _fbp=fb.1.1608927047791.241076104; g_state={"i_p":1609027947974,"i_l":2}; __gads=ID=a16361a759eff615:T=1608941572:S=ALNI_MYPE5vek-18b9AK9aDFpwVFxhIEsQ; ki_r=; ki_s=; ki_t=1608943863559%3B1608943863559%3B1608944617005%3B1%3B5; zgsession=1|f7b14e31-9d08-428f-b4a8-000e9c2d56d2; _gid=GA1.2.2095268098.1610576332; JSESSIONID=B1DEB1763434971B5EA390752C82F0F3; KruxPixel=true; DoubleClickSession=true; _derived_epik=dj0yJnU9bGJqZ05pYWk5Rl9aWHJDdHZ5QUFaS2Nnajhra3NGOV8mbj1ja2M4ODl0bWFYSHJpNndIdHlQN1RBJm09NyZ0PUFBQUFBRl9fY2Mw; _px3=4096574870da9a1b26fc09cde1426839cc15e8a864d5bb187d5fa27c0c74fd19:5g7EPWaEGeBTHB+B5dmVtcOJQLUBPLAeUhUI5jl4QnMaFvxh6AkZzSzQEk3y27pMLIeMGFrOwKqKbWnNQAOnbA==:1000:R3QDIVj/RvCUxdTjWHEO2g2pSTxi2ezGLUC4WlSnHb2FeGwTGd+sb7Kyh6nPb6i+AWxJvz9PdVXO72O5gF1VUMeEZipwBIWwFKQ7jeDrTcqLVqj7NVAU0ghGxL/1TCtV0DdQ1BEqWRifWWdCu+e35OgNLosNh3iJ3R+PZVUnErk=; _uetsid=518bc75055ed11eba060f1050a2691e8; _uetvid=518c247055ed11ebb903c39933ba89c9; KruxAddition=true; AWSALB=YWSzHZDP1Pox78zrhAyWpOdD/tJtYLEIEIT2r85ZMSx0lhdn4kECz1V7jskx2QdALWzfiysh5W3k85mXjFJ0wBNvQPFoH4zm2p1he4i1TBU5m84XZVVaN6aR/9AI; AWSALBCORS=YWSzHZDP1Pox78zrhAyWpOdD/tJtYLEIEIT2r85ZMSx0lhdn4kECz1V7jskx2QdALWzfiysh5W3k85mXjFJ0wBNvQPFoH4zm2p1he4i1TBU5m84XZVVaN6aR/9AI; search=6|1613168420553%7Crect%3D26.15237739236255%252C-80.3470818249512%252C26.055107676288717%252C-80.46552817504886%26rid%3D7886%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%097886%09%09%09%09%09%09; _gat=1',
        'Host' : 'www.zillow.com',
        'Referer' : 'https://www.zillow.com/homes/weston_rb/',
        'Sec-Fetch-Dest' : 'document',
        'Sec-Fetch-Mode' : 'navigate',
        'Sec-Fetch-Site' : 'same-origin',
        'Sec-Fetch-User' : '?1',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/'
    }

    def fetch(self, url, params): #fethches response
        response = requests.get(url, headers = self.headers, params = params)
        print(response)
        return response

    def parse(self, response): #function to parse the data, using Beautiful Soup
        content = BeautifulSoup(response)
        deck = content.find('ul', {'class' : 'photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution'})
        for card in deck.contents:
            script = card.find('script', {'type' : 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])

                self.results.append({ #extract the data that I am looking for, disregard the rest
                    'Address' : script_json['name'],
                    #'Sq Footage' : script_json['floorSize']['value']
                    'Price' : card.find('div', {'class' : 'list-card-price'}).text,
                    'Info' : card.find('ul', {'class' : 'list-card-details'}).text,
                    'URL' : script_json['url']
                })

    def to_csv(self): #function to write data to a csv file
        with open('Houses in Weston.csv', 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = self.results[0].keys())
            writer.writeheader()

            for row in self.results:
                writer.writerow(row)

    def run(self):
        url = 'https://www.zillow.com/homes/weston_rb/'

        for page in range(1, 8):
            params = {
                'searchQueryState' : '{"pagination":{"currentPage": %s},"usersSearchTerm":"weston","mapBounds":{"west":-80.46552817504886,"east":-80.3470818249512,"south":26.055107676288717,"north":26.15237739236255},"regionSelection":[{"regionId":7886,"regionType":6}],"isMapVisible":false,"filterState":{"sort":{"value":"globalrelevanceex"},"ah":{"value":true}},"isListVisible":true,"mapZoom":13}' %page
            } 
            res = self.fetch(url, params)
            self.parse(res.text)
            time.sleep(2)
        self.to_csv() #writing to csv file

if __name__ == "__main__":
    scraper = ZillowScraper()
    scraper.run()
