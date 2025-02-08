import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import csv

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-notifications")

URL = "https://www.youtube.com/@Toyz69/videos"
video_to_scrape = URL  # Provide YT Video URL

driver = webdriver.Chrome("./chromedriver.exe", chrome_options=chrome_options)
driver.get(URL)

SCROLL_PAUSE_TIME = 2
delay = 5  #30
scrolling = True
last_height = driver.execute_script("return document.documentElement.scrollHeight")
scrolling_attempt = 2  # 5

xpath = ""
xpath1 = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/"\
         "div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-item-renderer["  # change this for each row
xpath2 = "]/div/ytd-rich-grid-media/div[1]/div[1]/ytd-thumbnail/a"

def scrape_loaded_comments():
    loaded_comments = []
    all_usernames = WebDriverWait(driver, delay).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="author-text"]/span')))
    all_comments = WebDriverWait(driver, delay).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@id="content-text"]/span')))
    try:
        all_usernames = all_usernames[-20:]
        all_comments = all_comments[-20:]
        
    except:
        print("could not get last 20 elements")

    for (username, comment) in zip(all_usernames, all_comments):
        current_comment = {"username": username.text,
                           "comment": comment.text}
        print(f"Username : {username.text}\nComment : {comment.text}")
        loaded_comments.append(current_comment)

    return loaded_comments
	
for row in range(10):
    time.sleep(3)
    xpath = xpath1 + str(row + 1) + xpath2
    print(xpath)
    all_comments_list = []
    element = WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
    time.sleep(1)
    num_of_comment = 0

    count = 0 ;        
    while scrolling:
        htmlelement = driver.find_element_by_tag_name("body")
        htmlelement.send_keys(Keys.END)
        try:
            last_20_comments = scrape_loaded_comments()
            all_comments_list = all_comments_list + last_20_comments
        except:
            print("error while trying to load comments")

        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        time.sleep(SCROLL_PAUSE_TIME)
        driver.implicitly_wait(30)

        if new_height == last_height:
            scrolling_attempt -= 1
            print(f"scrolling_attempt {scrolling_attempt}")
            if scrolling_attempt == 0:
                scrolling = False

        last_height = new_height

        new_all_comment_list = []
        matches = ["TOYZ", "Toyz", "toyz" ,"椅子", "詐欺", "小劉", "拖椅子"]
        for comment in all_comments_list:
            if comment not in new_all_comment_list :
                if any([keyword in comment["comment"] for keyword in matches]) :
                    new_all_comment_list.append(comment)

        df = pd.DataFrame(new_all_comment_list)
        df.to_csv(os.path.join("excel/", f"comment_{10-row}.csv"), encoding="utf_8_sig", index=False)
      
    driver.back()
    scrolling_attempt = 2
    scrolling = True
    time.sleep(2)
    
driver.quit()