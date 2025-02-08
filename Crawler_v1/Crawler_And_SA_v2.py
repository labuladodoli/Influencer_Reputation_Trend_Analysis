import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


URL = "https://www.youtube.com/@Toyz69/videos"
#URL = "https://www.youtube.com/@LadyFlavor/videos"
video_to_scrape = URL # Provide YT Video URL

driver = webdriver.Chrome("C:/Users/user/Desktop/chromedriver.exe")
driver.get(video_to_scrape)

SCROLL_PAUSE_TIME = 2
delay = 5 #30
scrolling = True
last_height = driver.execute_script("return document.documentElement.scrollHeight")
all_comments_list = []
scrolling_attempt = 5 # 5

xpath = ""
xpath1 = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/"\
         "div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row["
xpath2 = "]/div/ytd-rich-item-renderer["
xpath3 = "]"

def scrape_loaded_comments():
    loaded_comments = []
    all_usernames = WebDriverWait(driver,delay).until(
        EC.presence_of_all_elements_located((By.XPATH, '//h3[@class="style-scope ytd-comment-renderer"]')))
    all_comments = WebDriverWait(driver,delay).until(
        EC.presence_of_all_elements_located((By.XPATH, '//yt-formatted-string[@id="content-text"]')))
    try :
        all_comments = all_comments[-20:]
        all_usernames = all_usernames[-20:]
    except :
        print("could not get last 20 elements")


    for (username, comment) in zip(all_usernames, all_comments):
        current_comment = {"username" : username.text,
                           "comment" : comment.text}
        print(f"Username : {username.text}\nComment : {comment.text}")
        loaded_comments.append(current_comment)
    
    return loaded_comments

for row in range(10):
    if ( not row == 0 and row %10 == 0 ):
        htmlelement = driver.find_element_by_tag_name("body")
        htmlelement.send_keys(Keys.END)
        time.sleep(2)
    for col in range(3):
        time.sleep(3)
        xpath = xpath1 + str(row+1) + xpath2 + str(col+1) + xpath3
        print(xpath)
        element = WebDriverWait(driver,delay).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        time.sleep(5)

        while scrolling == True:
            htmlelement = driver.find_element_by_tag_name("body")
            htmlelement.send_keys(Keys.END)
            try:
                last_20_comments = scrape_loaded_comments()
                all_comments_list = all_comments_list + last_20_comments 
            except:
                print( "error while trying to load comments" )
    
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            time.sleep(SCROLL_PAUSE_TIME)
            driver.implicitly_wait(30)
    
            if new_height == last_height:
                scrolling_attempt -= 1
                print(f"scrolling_attempt {scrolling_attempt}")
                if ( scrolling_attempt == 0 ):
                    scrolling = False
            
            last_height = new_height

        driver.back()
        scrolling_attempt = 5
        scrolling = True
        time.sleep(2)


new_all_comment_list = []
matches = ["TOYZ", "Toyz", "toyz" ,"椅子", "詐欺", "小劉", "拖椅子"]
for comment in all_comments_list:
    if comment not in new_all_comment_list :
        if any([keyword in comment["comment"] for keyword in matches]) :
            new_all_comment_list.append(comment)
            #print( "yaya", comment["comment"])

score = 0 
from paddlenlp import Taskflow
from opencc import OpenCC

cc = OpenCC('t2s')
#senta = Taskflow("sentiment_analysis", model="skep_ernie_1.0_large_ch")
senta = Taskflow("sentiment_analysis")

for comment in new_all_comment_list:
    try:
        if senta(cc.convert(comment["comment"]))[0]['label'] == 'positive':
            score += float(senta(cc.convert(comment["comment"]))[0]['score'])
        elif senta(cc.convert(comment["comment"]))[0]['label'] == 'negative':
            score -= float(senta(cc.convert(comment["comment"]))[0]['score'])
    except ZeroDivisionError:
        print( "it occurs a ZeroDivisionError" )

print( "favorable_rating : ", score )

