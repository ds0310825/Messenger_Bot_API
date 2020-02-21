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

    driver.get(chat_room_url)
    print(chat_room_url)
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

    i2_last = 0

    # os.system('cls')

    print('running')

    input_mes = ''

    while True:
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
                print('msg_test error')
                print(e)

            try:
                for command, reply in command_list.items():
                    msg_printer(command, reply)
            except Exception as e:
                print('command error')
                print(e)

            try:
                nhentai_search()
            except Exception as e:
                print('nh error')
                print(e)

            try:
                sankaku_search()
            except Exception as e:
                print('sankaku error')
                print(e)

            try:
                san_nsfw_check()
            except Exception as e:
                print('sankaku_nsfw error')
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
