from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import xmltojson
import json
import requests
import time
import os
from datetime import datetime
from time import strftime   


def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


def PingMe(s):
    token = ""
    url = f"https://api.telegram.org/bot{token}"
    params = {"chat_id": "1171744631", "text": s}
    try:
        r = requests.get(url + "/sendMessage", params=params)
        print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), r.content)
        pass
    except Exception as e:
        print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), e)


def Scrap():
    driver_path = '/home/manohar/Downloads/chromedriver_linux64/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

    driver.get('https://www.cowin.gov.in/home')

    pin_code = '121009'
    # pin_code = '110001'

    try:
        input_element = driver.find_element_by_id('mat-input-0')
        input_element.send_keys(pin_code)

        search_button = driver.find_element_by_class_name('pin-search-btn')
        search_button.click()
    except:
        msg = "Hey Manohar, Please check your console logs. Your program has stopped!"
        print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), msg)
        PingMe(msg)
        os.system(f'spd-say "{msg}"')

    try:
        appointment_element = driver.find_element_by_class_name('appointment-msg')
        html_content = appointment_element.get_attribute('innerHTML')
        json_string = xmltojson.parse(html_content)
        json_content = json.loads(json_string)
        print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), json_content['p']['#text'])
    except:
        print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), 'No appointment message')

    try:
        slots_element = driver.find_element_by_class_name('mat-main-field')
        html_content = slots_element.get_attribute('innerHTML')
        json_string = xmltojson.parse(html_content)
        json_content = json.loads(json_string)
        center_list = json_content['div']['div']

        msg = ""
        for center in center_list:
            center_name = center['div']['div']['div'][0]['div']['h5']['#text']
            center_address = center['div']['div']['div'][0]['div']['p']['#text']
            week_slots = center['div']['div']['div'][1]['ul']['li']
            new_center = True
            for slot in week_slots:
                vaccine_box = slot['div']['div']
                if 'a' in vaccine_box:
                    available_slots = vaccine_box['a']['#text']
                else:
                    available_slots = vaccine_box['div'][0]['a']['#text']
                if available_slots.isnumeric():
                    if new_center:
                        msg = msg + center_name + ' - ' + center_address + ': '
                        new_center = False
                    msg = msg + available_slots + ', '
            if not new_center:
                msg = msg + '\n'
        if len(msg) > 0:
            print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), msg)
            PingMe(msg)
            os.system(f'spd-say "{msg}"')
        else:
            print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), 'Slots fully booked!')

    except:
        print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), 'Unable to get slot list')

    driver.quit()


def main():
    while True:
        try:
            Scrap()
            time.sleep(10)
        except:
            msg = "terminated!"
            print(datetime.now().strftime("[%Y-%m-%d %H:%M:%S]"), msg)
            PingMe(msg)
            os.system(f'spd-say "{msg}"')
            raise


if __name__ == "__main__":
    main()
