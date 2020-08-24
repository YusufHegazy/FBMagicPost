import json
import facebook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

fb_email = "" 
fb_pass = ""
token = ""
post_id = ""
user_id = ""
edge_path = ""
driver = webdriver.Edge(edge_path)

def fetch_likes_and_cmts():

    graph = facebook.GraphAPI(token)

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
    driver.get("https://mbasic.facebook.com/")
    email_form = driver.find_element_by_id("m_login_email")
    pass_form = driver.find_element_by_name("pass")
    login_btn = driver.find_element_by_name("login")
    email_form.send_keys(fb_email)
    pass_form.send_keys(fb_pass)
    login_btn.click()
    WebDriverWait(driver, 20).until(EC.title_is("Facebook"))
    logging.info("Logged In!")

old_reacts, old_cmts = 0, 0

def editPostFn():
    global old_reacts
    global old_cmts
    driver.get("https://mbasic.facebook.com/story.php?story_fbid={}&id={}".format(post_id, user_id))
    editpost_textbox_xpath = "/html/body/div/div/div[2]/div[2]/div[1]/form/textarea"
    save_btn_xpath = "/html/body/div/div/div[2]/div[2]/div[1]/form/div/input"
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.LINK_TEXT, "Edit"))).click()
    reacts, cmts = fetch_likes_and_cmts()

    if (old_reacts == reacts and old_cmts == cmts):
        logging.info("No changes! skipping this round..")
    else:
        post_text = "البوست دا بيحدث نفسه لوحده و فيه دلوقتي {} رياكت و {} كومنت".format(reacts, cmts)
        maintenance = " ---- جاري صيانه البوست سنعود بعد قليل ---- "
        WebDriverWait(driver, 20).until(EC.title_is("Edit Post"))
        edit_form = driver.find_element_by_xpath(editpost_textbox_xpath)
        edit_form.clear()
        edit_form.send_keys(post_text)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, save_btn_xpath))).click()
        logging.info("Edited")
    old_reacts, old_cmts = reacts, cmts


def mainLoop():
    try:
        loginFn()

        while True:
            editPostFn()
            logging.info("Sleeping for 40 Seconds........")
            time.sleep(40)

    except:
        logging.info("OHFUCK AN EXCEPTION!.. Sleeping for 5 mins")
        time.sleep(300)
        mainLoop()

mainLoop()
