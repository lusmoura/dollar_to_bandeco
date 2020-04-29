import credentials

import requests
from requests_html import HTMLSession

from time import sleep
from datetime import datetime

import json
import tweepy

class Currency:
    def get_coin(self, name):
        url = f'https://www.google.com/search?q={name}+moeda'
        session = HTMLSession()
        request = session.get(url)
        selector = '#knowledge-currency__updatable-data-column > div.b1hJbf > div.dDoNo.vk_bk.gsrt > span.DFlfde.SwHCTb'
        value_text = request.html.find(selector, first=True).text
        value = float(value_text.replace(',', '.'))
        
        return value

    def get_dollar(self):
        return self.get_coin('dolar')

    def get_euro(self):
        return self.get_coin('euro')

    def get_libra(self):
        return self.get_coin('libra')

class Values:
    def __init__(self):
        self.currency = Currency()
        self.dollar = 0
        self.euro = 0
        self.libra = 0
        self.last_dollar = 0
        self.last_euro = 0
        self.last_libra = 0

    def update_last_values(self):
        self.last_dollar = self.dollar
        self.last_euro = self.euro
        self.last_libra = self.libra

    def get_new_values(self):
        self.dollar = self.currency.get_dollar()
        self.euro = self.currency.get_euro()
        self.libra = self.currency.get_libra()

    def get_joke(self, val, last_val):
        if val > last_val:
            return 'já dá pra mais que antes =D'
        elif val < last_val:
            return 'não dá pra tanto quanto antes =(()'
        else:
            return "ta na mesma '-'"

    def get_text(self):
        hora = datetime.now().strftime('%H:%M')

        self.update_last_values()
        self.get_new_values()

        text = ""
        text += f'Às {hora}\n'
        text += f'1 dólar = {self.dollar/2} bandecos, {self.get_joke(self.dollar, self.last_dollar)}\n'
        text += f'1 euro = {self.euro/2} bandecos, {self.get_joke(self.euro, self.last_euro)}\n'
        text += f'1 libra = {self.libra/2} bandecos, {self.get_joke(self.libra, self.last_libra)}\n'

        return text

class Bot:
    def __init__(self):
        api_key = credentials.api_key 
        api_secret = credentials.api_secret 
        access_token = credentials.access_token
        access_token_secret = credentials.access_token_secret
    
        auth = tweepy.OAuthHandler(api_key, api_secret) 
        auth.set_access_token(access_token, access_token_secret)
        self.values = Values()
        self.api = tweepy.API(auth)

    def post_tweet(self):
        tweet = self.values.get_text()
        self.api.update_status(tweet)

if __name__ == '__main__':
    bot = Bot()

    while (True):
        bot.post_tweet()
        sleep(10)