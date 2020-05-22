import requests
import sys
import re
import os
import threading
import sqlite3
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import *
from messenger_bot_ui import Ui_Dialog

# from main import run

global command_list
command_list = {}


def run(account, password, chat_room_url, command_list):
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from time import sleep
    import random
    from urllib.request import urlopen
    import urllib
    import requests
    import selenium.webdriver.support.ui as ui
    import warnings

    warnings.filterwarnings('ignore')

    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument('--headless')

    driver = webdriver.Chrome(chrome_options=options)

    # driver = webdriver.Chrome()

    driver.get("https://www.facebook.com/login")
    driver.find_element_by_id("email").click()
    driver.find_element_by_id("email").clear()
    driver.find_element_by_id("email").send_keys(account)
    driver.find_element_by_id("pass").click()
    driver.find_element_by_id("pass").clear()
    driver.find_element_by_id("pass").send_keys(password)
    driver.find_element_by_id("pass").send_keys(u'\ue007')

    # wait = ui.WebDriverWait(driver, 10)
    sleep(10)
    driver.get(chat_room_url)
    print(chat_room_url)
    # driver.click()
    wait = ui.WebDriverWait(driver, 10)

    san_nsfw_state = True

    def san_nsfw_check():
        global san_nsfw_state
        if input_mes == "nsfw san off":
            san_nsfw_state = False
            driver.switch_to_active_element().send_keys("NSFW:OFF")
            driver.switch_to_active_element().send_keys(u'\ue007')

        elif input_mes == "nsfw san on":
            san_nsfw_state = True
            driver.switch_to_active_element().send_keys("NSFW:ON")
            driver.switch_to_active_element().send_keys(u'\ue007')

    def msg_printer(input, output):
        if input_mes == input:
            driver.switch_to_active_element().send_keys(output)
            driver.switch_to_active_element().send_keys(u'\ue007')

    def nhentai_search():
        try:
            not_found_state = True

            inputs = input_mes.split(' ')

            try:
                int(inputs[1])
                six_num_checked = True
            except:
                six_num_checked = False

            if inputs[0] == 'nh' and len(inputs) <= 1:
                nh_url = "https://nhentai.net/g/" + str(random.randint(100000, 300000))
                driver.switch_to_active_element().send_keys(nh_url)
                not_found_state = False
                wait.until(lambda driver: driver.find_element_by_css_selector("[class='_4yp9']"))
                driver.switch_to_active_element().send_keys(u'\ue007')
                print(input_mes[2:])

            elif inputs[0] == 'nh' and len(inputs) == 2 and six_num_checked == True:
                driver.switch_to_active_element().send_keys('https://nhentai.net/g/{}/'.format(inputs[1]))
                not_found_state = False
                wait.until(lambda driver: driver.find_element_by_css_selector("[class='_4yp9']"))

                driver.switch_to_active_element().send_keys(u'\ue007')

            elif inputs[0] == 'nh' and len(inputs) > 1:
                nh_url = "https://nhentai.net/search/?q=" + "+".join(inputs[1:])
                print('searching:', nh_url)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                req = urllib.request.Request(url=nh_url, headers=headers)

                html = urlopen(req).read()
                review = BeautifulSoup(html, 'lxml')
                # review_imgs_html = review.findAll('img', attrs={'is': 'lazyload-image'})
                review_urls_html = review.findAll('a', attrs={'class': 'cover'})
                random_int = random.randint(0, review_urls_html.__len__())
                # review_img = review_imgs_html[random_int]
                review_url = review_urls_html[random_int]
                # review_img = review_img['data-src']
                review_url = review_url['href']

                # r = requests.get(review_img)
                # with open('review.jpg', "wb") as code:
                #     code.write(r.content)

                driver.switch_to_active_element().send_keys('https://nhentai.net' + review_url)
                # print('wait')
                wait.until(lambda driver: driver.find_element_by_css_selector("[class='_4yp9']"))

                not_found_state = False

                print('\n')
                # driver.find_element_by_css_selector("[class='_260t _n _2__f _4e5e']").send_keys(
                #     r'C:\Users\player-2\PycharmProjects\Crawler\review.jpg')
                driver.switch_to_active_element().send_keys(u'\ue007')

        except Exception as e:
            if not_found_state:
                print('download error')
                print('\n!!!', e)
                driver.switch_to_active_element().send_keys(" " + " ".join(inputs[1:]) + r' Not Found!!!')
            driver.switch_to_active_element().send_keys(u'\ue007')

    def sankaku_search():
        try:
            not_found_state = True

            inputs = input_mes.split(' ')

            if inputs[0] == 'san' and len(inputs) > 1:
                san_url = "https://chan.sankakucomplex.com/?tags="
                san_url += "+".join(inputs[1:])
                if not san_nsfw_state:
                    san_url += "+rating%3Asafe"
                san_url += "&commit=Search"
                print('searching:', san_url)
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
                req = urllib.request.Request(url=san_url, headers=headers)

                html = urlopen(req).read()
                review = BeautifulSoup(html, 'lxml')
                # review_imgs_html = review.findAll('img', attrs={'is': 'lazyload-image'})
                review_urls_html = review.findAll('span', attrs={'class': 'thumb'})
                random_int = random.randint(0, review_urls_html.__len__())
                # review_img = review_imgs_html[random_int]
                review_url = review_urls_html[random_int]
                # review_img = review_img['data-src']
                review_url = review_url['id']

                # r = requests.get(review_img)
                # with open('review.jpg', "wb") as code:
                #     code.write(r.content)

                driver.switch_to_active_element() \
                    .send_keys(r"https://chan.sankakucomplex.com/post/show/" + review_url[1:])

                not_found_state = False

                # sleep(5)
                wait.until(lambda driver: driver.find_element_by_css_selector("[class='_4yp9']"))
                # driver.find_element_by_css_selector("[class='_260t _n _2__f _4e5e']").send_keys(
                #     r'C:\Users\player-2\PycharmProjects\Crawler\review.jpg')
                driver.switch_to_active_element().send_keys(u'\ue007')

        except Exception as e:
            if not_found_state:
                print('error')
                print('\n!!!', e)
                driver.switch_to_active_element().send_keys(" " + " ".join(inputs[1:]) + r' Not Found!!!')
            driver.switch_to_active_element().send_keys(u'\ue007')

    def cat_search():
        try:
            if input_mes == 'cat':
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}
                req = urllib.request.Request(url=r'https://unsplash.com/images/animals/cat', headers=headers)

                html = urlopen(req).read()
                review = BeautifulSoup(html, 'lxml')
                images = review.findAll('img', attrs={'class': '_2zEKz'})
                print(len(images))
                driver.switch_to_active_element().send_keys(images[random.randint(1, len(images) - 1)]['src'])
                wait.until(lambda driver: driver.find_element_by_css_selector("[class='_4yp9']"))
                driver.switch_to_active_element().send_keys(u'\ue007')
        except Exception as e:
            print('error')
            print('\n!!!', e)

    def send_pig():
        inputs = input_mes.split(' ')
        if inputs[0] == 'pig':

            sleep(1)
            driver.find_element_by_class_name('_7mki').click()
            sleep(1)
            driver.find_elements_by_class_name('_7oal')[8].click()
            sleep(1)
            driver.find_elements_by_class_name('_5r8a')[2].click()
            sleep(1)
            for _ in range(int(inputs[2]) if int(inputs[2]) <= 5 else 5):
                driver.find_elements_by_class_name('_5r8i')[int(inputs[1])].click()
                sleep(0.2)

            driver.switch_to_active_element().send_keys('---UWU---')
            driver.switch_to_active_element().send_keys(u'\ue007')

    i2_last = 0

    # os.system('cls')

    # sleep(20)

    print('running')

    input_mes = ''

    while True:
        # wait.until(lambda driver: driver.find_element_by_css_selector("[class='_58nk']"))
        i2 = driver.find_elements_by_class_name('_58nk')
        try:
            if i2_last == i2:
                continue
            # print(len(i2))
            input_mes = i2[-1].text
            print(input_mes)
            i2_last = i2
        except Exception as e:
            print(e)

        try:
            try:
                msg_printer('bot test', "測試成功")
            except Exception as e:
                print('msg_test')
                print(e)

            try:
                for command, reply in command_list.items():
                    msg_printer(command, reply)
            except Exception as e:
                print('command')
                print(e)

            try:
                nhentai_search()
            except Exception as e:
                print('nh')
                print(e)

            try:
                sankaku_search()
            except Exception as e:
                print('sankaku')
                print(e)

            try:
                san_nsfw_check()
            except Exception as e:
                print('sankaku_nsfw')
                print(e)

            try:
                send_pig()
            except Exception as e:
                print('pig')
                print(e)

            try:
                cat_search()
            except Exception as e:
                print('cat')
                print(e)

        except:
            pass

        sleep(0.5)
        # driver.refresh()


class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.open.clicked.connect(self.start)
        self.ui.add_command.clicked.connect(self.add_command)
        self.ui.delete_selected.clicked.connect(self.delete_command)

        script_dir = os.path.dirname(__file__)
        abs_dir_path = os.path.join(script_dir, "messenger_bot_data")
        abs_file_path = os.path.join(abs_dir_path, "account_info")
        abs_db_path = os.path.join(abs_dir_path, "command.db")
        try:
            if not os.path.exists(abs_dir_path):
                os.mkdir(abs_dir_path)
            if not os.path.exists(abs_file_path):
                open(abs_file_path, 'w+')

            self.db = sqlite3.connect(abs_db_path)

            try:
                self.db.execute("create table command_table "
                                "(command text,"
                                "reply text)")
            except:
                pass

            self.load_command()

        except Exception as e:
            print(e)

        with open(abs_file_path, 'r') as record:
            self.ui.account.setText(record.readline().strip())
            self.ui.password.setText(record.readline().strip())
            self.ui.chat_room_url.setText(record.readline().strip())

        self.show()

    def load_command(self):
        c = self.db.cursor()
        command_table = c.execute('select * from command_table')
        rows = command_table.fetchall()

        for (command, reply) in rows:
            command_list[command] = reply

        # print(command_list)

        slm = QStringListModel()
        listview_items = ["{}  :  {}".format(command, reply) for command, reply in command_list.items()]
        slm.setStringList(listview_items)

        self.ui.command_listview.setModel(slm)

    def start(self):
        script_dir = os.path.dirname(__file__)
        abs_dir_path = os.path.join(script_dir, "messenger_bot_data")
        abs_file_path = os.path.join(abs_dir_path, "account_info")

        with open(abs_file_path, 'w') as record:
            record.write('\n'.join([self.ui.account.text(), self.ui.password.text(), self.ui.chat_room_url.text()]))

        self.close()
        run(self.ui.account.text(), self.ui.password.text(), self.ui.chat_room_url.text(), command_list)

    def add_command(self):
        slm = QStringListModel()

        command_list[self.ui.command.text()] = self.ui.reply.text()

        c = self.db.cursor()
        c.execute("insert into command_table "
                  "values (?, ?)", (self.ui.command.text(), self.ui.reply.text()))
        self.db.commit()
        listview_items = ["{}  :  {}".format(command, reply) for command, reply in command_list.items()]
        slm.setStringList(listview_items)

        self.ui.command_listview.setModel(slm)

        # print(command_list)

    def delete_command(self):
        slm = QStringListModel()

        selected_command = self.ui.command_listview.selectedIndexes()

        selected_command = selected_command[0].data().split('  :  ')[0].strip()
        # print(selected_command)

        del command_list[selected_command]

        c = self.db.cursor()

        c.execute("delete from command_table "
                  "where command = ?", (selected_command,))
        self.db.commit()
        listview_items = ["{}  :  {}".format(command, reply) for command, reply in command_list.items()]
        slm.setStringList(listview_items)

        self.ui.command_listview.setModel(slm)

        # print(command_list)


import zipfile
import os
import json
import logging
from win32com import client as wincom_client
import requests

CHROME_DRIVER_BASE_URL = "https://chromedriver.storage.googleapis.com"
CHROME_DRIVER_FOLDER = r"."
CHROME_DRIVER_MAPPING_FILE = r"{}\mapping.json".format(CHROME_DRIVER_FOLDER)
CHROME_DRIVER_EXE = r"{}\chrmoedriver.exe".format(CHROME_DRIVER_FOLDER)
CHROME_DRIVER_ZIP = r"{}\chromedriver_win32.zip".format(CHROME_DRIVER_FOLDER)


def get_file_version(file_path):
    logging.info('Get file version of [%s]', file_path)
    if not os.path.isfile(file_path):
        raise FileNotFoundError("{!r} is not found.".format(file_path))

    wincom_obj = wincom_client.Dispatch('Scripting.FileSystemObject')
    version = wincom_obj.GetFileVersion(file_path)
    logging.info('The file version of [%s] is %s', file_path, version)
    return version.strip()


def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def read_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def get_chrome_driver_major_version():
    chrome_browser_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_ver = get_file_version(chrome_browser_path)
    chrome_major_ver = chrome_ver.split(".")[0]
    return chrome_major_ver


def get_latest_driver_version(browser_ver):
    latest_api = "{}/LATEST_RELEASE_{}".format(
        CHROME_DRIVER_BASE_URL, browser_ver)
    resp = requests.get(latest_api)
    lastest_driver_version = resp.text.strip()
    return lastest_driver_version


def download_driver(driver_ver, dest_folder):
    download_api = "{}/{}/chromedriver_win32.zip".format(
        CHROME_DRIVER_BASE_URL, driver_ver)
    dest_path = os.path.join(dest_folder, os.path.basename(download_api))
    resp = requests.get(download_api, stream=True, timeout=300)

    if resp.status_code == 200:
        with open(dest_path, "wb") as f:
            f.write(resp.content)
        logging.info("Download driver completed")
    else:
        raise Exception("Download chrome driver failed")


def unzip_driver_to_target_path(src_file, dest_path):
    with zipfile.ZipFile(src_file, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    logging.info("Unzip [{}] -> [{}]".format(src_file, dest_path))


def read_driver_mapping_file():
    driver_mapping_dict = {}
    if os.path.exists(CHROME_DRIVER_MAPPING_FILE):
        driver_mapping_dict = read_json(CHROME_DRIVER_MAPPING_FILE)
    return driver_mapping_dict


def check_browser_driver_available():
    # if not os.path.isdir(CHROME_DRIVER_FOLDER):
    #     os.mkdir(CHROME_DRIVER_FOLDER)

    chrome_major_ver = get_chrome_driver_major_version()
    mapping_dict = read_driver_mapping_file()
    driver_ver = get_latest_driver_version(chrome_major_ver)

    if chrome_major_ver not in mapping_dict:
        download_driver(driver_ver, CHROME_DRIVER_FOLDER)
        unzip_driver_to_target_path(CHROME_DRIVER_ZIP, CHROME_DRIVER_FOLDER)

        mapping_dict = {
            chrome_major_ver: {
                "driver_path": CHROME_DRIVER_EXE,
                "driver_version": driver_ver
            }
        }
        mapping_dict.update(mapping_dict)
        write_json(CHROME_DRIVER_MAPPING_FILE, mapping_dict)


if __name__ == '__main__':
    check_browser_driver_available()

    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
