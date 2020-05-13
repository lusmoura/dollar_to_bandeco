import credentials

import requests
from requests_html import HTMLSession

from time import sleep
from datetime import datetime

import json
import tweepy
import pickle

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

    def get_text(self):
        hora = datetime.now().strftime('%H:%M')
        
        last_dollar = self.get_last_value()
        dollar = self.get_new_value()
        self.update_last_value(dollar)

        text = ""
        text += f'Às {hora}\n'
        text += f'1 dólar = {dollar/2} bandecos, {self.get_joke(dollar, last_dollar)}'

        return text

    def get_joke(self, val, last_val):
        if val > last_val:
            return 'já dá pra mais que antes =D'
        elif val < last_val:
            return 'não dá pra tanto quanto antes =(()'
        else:
            return "ta na mesma '-'"

    def get_last_value(self):
        try:
            infile = open('last_value.pickle', 'rb')
            last_val = pickle.load(infile)
            infile.close()
            return last_val
        except:
            return 0

    def update_last_value(self, last_val):
        outfile = open('last_value.pickle','wb')
        pickle.dump(last_val, outfile)
        outfile.close()

    def get_new_value(self):
        return self.currency.get_dollar()


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
    bot.post_tweet()