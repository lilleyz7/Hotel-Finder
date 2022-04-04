import requests

from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.tab import MDTabsBase
from ApiKey import get_api_key

my_tabs = {}


class Tab (MDFloatLayout, MDTabsBase):
    pass


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Blue"
        return WindowManager()

    def get_variables(self):
        city_name = self.root.ids.city.text.lower()
        min_price = self.root.ids.min.text
        max_price = self.root.ids.max.text
        sort_by = self.root.ids.sortBy.text.upper()

        if city_name != "" and min_price != "" and max_price != "" and sort_by != "":
            city_id = self.get_location(city_name)
            self.obtain_query(city_id, min_price, max_price, sort_by)

    def get_location(self, location_name):
        url = "https://hotels4.p.rapidapi.com/locations/search"

        querystring = {"query": location_name, "locale": "en_US"}

        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': "8a2d3f00c4msh43ba13fbd502ca5p1d3889jsn8bcad05f141a"
        }

        try:
            response = requests.request("GET", url, headers=headers, params=querystring)
            json_data = response.json()
            cityID = json_data["suggestions"][0]["entities"][0]["destinationId"]
            return cityID
        except requests.exceptions.RequestException as e:
            print(e)


    def obtain_query(self, city_id, min_price, max_price, sort_by):
        key = get_api_key()
        url = "https://hotels4.p.rapidapi.com/properties/list"
        page_size = 5

        querystring = {"destinationId": city_id,
                       "pageNumber": "1",
                       "pageSize": page_size,
                       "checkIn": "2020-01-08",
                       "checkOut": "2020-01-15",
                       "adults1": "1",
                       "priceMin": min_price,
                       "priceMax": max_price,
                       "sortOrder": sort_by,
                       "locale": "en_US",
                       "currency": "USD"}

        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': key
        }

        try:
            response = requests.get(url, headers=headers, params=querystring)
            json_data = response.json()

            i = 0

            while i < page_size:
                hotel_name = (json_data["data"]["body"]["searchResults"]["results"][i]["name"])
                hotel_rating = (json_data["data"]["body"]["searchResults"]["results"][i]["starRating"])
                hotel_address = (json_data["data"]["body"]["searchResults"]["results"][i]["address"]["streetAddress"])
                nightly_cost = (json_data["data"]["body"]["searchResults"]["results"][i]["ratePlan"]["price"]["current"])
                my_tabs[i] = hotel_name, hotel_rating, hotel_address, nightly_cost
                i += 1

        except requests.exceptions.RequestException as e:
            print(e)



    def set_second_screen(self):
        self.root.ids.label1.text = str(my_tabs[0][0])
        self.root.ids.hotel1_rating.text = "This location has a star rating of " + str(my_tabs[0][1])
        self.root.ids.hotel1_address.text = "The address is " + str(my_tabs[0][2])
        self.root.ids.hotel1_price.text = "The current lowest rate for the hotel is " + str(my_tabs[0][3])
        self.root.ids.label2.text = str(my_tabs[1][0])
        self.root.ids.hotel2_rating.text = "This location has a star rating of " + str(my_tabs[1][1])
        self.root.ids.hotel2_address.text = "The address is " + str(my_tabs[1][2])
        self.root.ids.hotel2_price.text = "The current lowest rate for the hotel is " + str(my_tabs[1][3])
        self.root.ids.label3.text = str(my_tabs[2][0])
        self.root.ids.hotel3_rating.text = "This location has a star rating of " + str(my_tabs[2][1])
        self.root.ids.hotel3_address.text = "The address is " + str(my_tabs[2][2])
        self.root.ids.hotel3_price.text = "The current lowest rate for the hotel is " + str(my_tabs[2][3])
        self.root.ids.label4.text = str(my_tabs[3][0])
        self.root.ids.hotel4_rating.text = "This location has a star rating of " + str(my_tabs[3][1])
        self.root.ids.hotel4_address.text = "The address is " + str(my_tabs[3][2])
        self.root.ids.hotel4_price.text = "The current lowest rate for the hotel is " + str(my_tabs[3][3])
        self.root.ids.label5.text = str(my_tabs[4][0])
        self.root.ids.hotel5_rating.text = "This location has a star rating of " + str(my_tabs[4][1])
        self.root.ids.hotel5_address.text = "The address is " + str(my_tabs[4][2])
        self.root.ids.hotel5_price.text = "The current lowest rate for the hotel is " + str(my_tabs[4][3])

    def clear_fields(self):
        self.root.ids.city.text = ""
        self.root.ids.min.text = ""
        self.root.ids.max.text = ""
        self.root.ids.sortBy.text = ""

if __name__ == "__main__":
    MyApp().run()