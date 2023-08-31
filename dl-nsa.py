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

def full_page_screenshot(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    parts = []
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to bottom
        time.sleep(random.uniform(2.1, 2.9)) # Wait to load page
        part = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        parts.append(part)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    # Combine images into one
    full_img = Image.new('RGB', (parts[0].width, sum(p.height for p in parts)))
    offset = 0
    for part in parts:
        full_img.paste(part, (0, offset))
        offset += part.height
    return full_img

def save_ss(article_no):
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
    driver.set_window_size(1920, 1080*4)
    driver.get(f"https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/{article_no}")
    #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    user_agent = driver.execute_script("return window.navigator.userAgent")
    is_webdriver = driver.execute_script("return window.navigator.webdriver")
    # Print the user agent
    time.sleep(random.uniform(5.5, 6.5))
    print("User Agent:", user_agent)
    print("Webdriver is", is_webdriver)
    image = full_page_screenshot(driver)
    image.save(f"article/{article_no}.png")

def main():
    os.system(f"mkdir articles > /dev/null 2>&1")

