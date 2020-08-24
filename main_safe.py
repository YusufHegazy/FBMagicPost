import json
import facebook
import requests
#from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#from pyvirtualdisplay import Display
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

#user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
# display = Display(visible=0, size=(800, 600))
# display.start()
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent={}".format(user_agent))

webdriver_path = "" #download from https://chromedriver.chromium.org/downloads

post_id = ""
user_id = ""

fb_email = ""
fb_pass = ""
fb_token = "" #get access token from fb dev tools and give user_posts perm

driver = webdriver.Chrome(webdriver_path)

def fetch_likes_and_cmts():

    graph = facebook.GraphAPI(fb_token)

    user_post_id = "{}_{}".format(user_id, post_id)

    reactions_endpoint = "{}/reactions".format(user_post_id)
    comments_endpoint = "{}/comments?filter=stream".format(user_post_id)


    post_reacts = graph.get_object(reactions_endpoint, summary=True)
    post_comments = graph.get_object(comments_endpoint, summary=True)

    logging.info("fetched likes and comments from api!")
    reacts_no = post_reacts["summary"]["total_count"]
    comments_no = post_comments["summary"]["total_count"]

    return reacts_no, comments_no


def loginFn():
    driver.get("https://m.facebook.com/")
    email_form = driver.find_element_by_xpath('//*[@id="m_login_email"]')
    pass_form = driver.find_element_by_xpath('//*[@id="m_login_password"]')
    login_btn = driver.find_element_by_xpath('//*[@id="u_0_4"]/button')
    email_form.send_keys(fb_email)
    pass_form.send_keys(fb_pass)
    login_btn.click()
    WebDriverWait(driver, 20).until(EC.title_is("Facebook"))


def editPostFn():
    driver.get("https://m.facebook.com/story.php?story_fbid={}&id={}".format(post_id, user_id))
    three_dots_xpath = "/html/body/div[1]/div/div[4]/div/div[1]/div/div/div/div[1]/header/div[2]/div/div/div[3]/div/a"
    edit_post_btn_xpath = "/html/body/div[1]/div/div[4]/div/div[4]/div/div/div[2]/a[18]"
    editpost_word_xpath = "/html/body/div[2]/div/div[1]/div/div[2]/div/div"
    editpost_textbox_xpath = "/html/body/div[2]/div/div[2]/div/form/div/textarea"
    save_btn_xpath = "/html/body/div[2]/div/div[1]/div/div[3]/div/button"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, three_dots_xpath))).click()
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, edit_post_btn_xpath))).click()
    reacts, cmts = fetch_likes_and_cmts()
    post_text = "البوست دا فيه {} رياكت و {} كومنت".format(reacts, cmts)
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, editpost_word_xpath), "Edit Post"))
    edit_form = driver.find_element_by_xpath(editpost_textbox_xpath)
    edit_form.clear()
    edit_form.send_keys(post_text)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, save_btn_xpath))).click()


loginFn()

while True:
    editPostFn()
    time.sleep(20)
