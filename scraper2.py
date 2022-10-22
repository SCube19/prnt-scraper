from email import header
import shutil
from bs4 import BeautifulSoup
import base64
import string
import requests
import os
import urllib.request
from urllib.error import HTTPError
import threading

URL = "http://www.prnt.sc/"
headers = {
    'authority': 'prnt.sc',
    'method': 'GET',
    'path': '/mt3343',
    'scheme': 'https',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'cookie': '_ga=GA1.2.741541427.1658092557; _gid=GA1.2.2058255352.1658092557; euconsent-v2=CPcQSoAPcQSoAAKAqAENCYCsAP_AAH_AAAwII6td_X__bX9j-_5_aft0eY1P9_r37uQzDhfNs-8F3L_W_LwXw2E7NF36pq4KmR4Eu1LBIQNlHMHUDUmwaokVrzHsak2cpyNKJ7JEknMZO2dYGF9Pn1lDuYKY7_5_9_bx2D-t_9_-39T378Xf3_dp_2_--vCfV599jfn9fV_789KP9__9v-_8__________3_4I7AEmGrcQBdmWODNoGEUKIEYVhIVQKACCgGFogsAHBwU7KwCXWELABAKkIwIgQYgowYBAAIJAEhEAEgBYIBEARAIAAQAIgEIACJgEFgBYGAQAAgGhYgBQACBIQZEBEcpgQFQJBQS2ViCUFehphAHWeAFAojYqABEkgIpAQEhYOAYAkBLxZIGmKF8gBGCFAKJUAA.YAAAAAAAAAAA; __qca=P0-4664673-1658093049820; __gads=ID=1330d9fd792a2a57:T=1658093129:S=ALNI_MaHD9Hl1ighmmpJZMEVq6OG6k5hcA; cto_bundle=U6QhIV9XOXdTSDhsTHFRU1RKcTN6MXozUDBCVUZxU29iOExONElZZ2xTcXVRS1FwcHBsMmR1UnNLblA4enBjeFFLSnBHc0V2ZTB6NTRoblB5dkJobHJnc1o4a1dmdGVzekhST2xuZWU0RXZJeiUyQkRaWTFIN0ZoNTMxUG0lMkJENnNlRlR3c3NmZm1wU1B3dkd0YXlkV3RwaVpYelN3JTNEJTNE; _gat=1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36'
}

downloader = urllib.request.URLopener()
downloader.addheader('User-Agent', 'Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36')

def scrape(l1, l2, n):
    path = f"images/{l1}{l2}"
    if not os.path.exists(path):
        os.makedirs(path)
    numeric = f"000{str(n)}"[-4:]
    id = f"{l1}{l2}{numeric}"
    fullpath = f"{path}/{id}"
    if os.path.exists(fullpath):
        return
    headers['referer'] = f"{URL}{id}"
    response = requests.get(f"{URL}{id}", headers=headers)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    image = soup.find("img", class_="screenshot-image")['src']
    try: 
        downloader.retrieve(image, fullpath)
    except (requests.exceptions.ConnectionError, ValueError, HTTPError):
        print(f"Image with id {id} was probably removed")

def allLetters(lowerBound, upperBound):
    for l1 in string.ascii_lowercase:
        for l2 in string.ascii_lowercase:
            for n in range(lowerBound, upperBound + 1):
                scrape(l1, l2, n)

def customLetters(lowerBound, upperBound, letters):
    for n in range(lowerBound, upperBound + 1):
        scrape(letters[0], letters[1], n) 
                 
lowerBound = int(input("Define lower adress number bound (inclusive): "))
upperBound = int(input("Define upper adress number bound (inclusive): "))
if lowerBound > upperBound:
    exit()
lowerBound = max(0, lowerBound)
upperBound = min(9999, upperBound)

mode = int(input("Mode:\n1. all adress letters\n2. choose custom adress letters"))
if mode > 2 or mode < 1:
    exit()

if mode == 1:
    allLetters(lowerBound, upperBound)
else:
    letters = input("Input your custom adress letters (2): ")
    if len(letters) != 2:
        exit()
    customLetters(lowerBound, upperBound, letters)


        

