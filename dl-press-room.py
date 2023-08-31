import sys
import os
import requests
import argparse
import concurrent.futures
import random
import time
from datetime import datetime
import re
import pickle
import csv
import io
from PIL import Image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

user_agent_list = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36']


def dl_article(article_num):
    chromedriver_executable = Service('chromedriver')
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--incognito")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument('--ignore-ssl-errors')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features")
    random_user_agent = random.choice(user_agent_list)
    options.add_argument(f"user-agent={random_user_agent}")
    driver = webdriver.Chrome(service = chromedriver_executable, options = options)
    driver.set_window_size(1920, 1080*3)    
    driver.get(f"https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/{article_num}")
    driver.save_screenshot(f"press-room/{article_num}.png")

def main():
    os.system('mkdir press-room > /dev/null 2>&1')
    with open('articles.txt', 'r') as f:
        articles_list = [line.strip() for line in f]
    for art in articles_list:
        dl_article(art)

if __name__ == "__main__":
    main()
