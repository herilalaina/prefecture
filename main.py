import os
import time
import random
import argparse
from selenium import webdriver

try:
    from twilio.rest import Client
except ImportError:
    print("Whatsapp notification not available. Please install and configure Twilio.")



def send_notification():
    account_sid = ''
    auth_token = ''
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='RDV FOUND',
        to='whatsapp:+0000000'
    )
    print(message.sid)


def reload(_browser):
    # True if not bad gateway
    page_ok = ("française" in _browser.find_element_by_tag_name('html').text.lower())
    c = 0
    while (not page_ok) and (c < 10):
        _browser.refresh()
        page_ok = ("française" in _browser.find_element_by_tag_name('html').text.lower())
        c += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RDV Prefecture')
    parser.add_argument(
        '--url',
        help='Link of the RDV webpage. e.g: https://www.essonne.gouv.fr/booking/create/23014/',
        type=str,
        required=True
    )
    parser.add_argument(
        '--delay', '-d',
        help='Delay in second between request.',
        type=int,
        default=30,
    )
    args = parser.parse_args()

    browser = webdriver.Firefox()
    found = False

    while not found:
        try:
            browser.get(args.url)
            browser.find_element_by_id("condition").click()
            browser.find_element_by_name("nextButton").click()
            reload(browser)
            while not found:
                porte_list = [elem.get_attribute("id") for elem in browser.find_elements_by_name("planning")]
                random.shuffle(porte_list)
                for id in porte_list:
                    time.sleep(args.delay)
                    browser.find_element_by_id(id).click()
                    reload(browser)

                    try:
                        browser.find_element_by_name("nextButton").click()
                        reload(browser)
                        if browser.find_element_by_id("inner_Booking").find_element_by_tag_name(
                                "h2").text == 'Description de la nature du rendez-vous':
                            browser.find_element_by_name("nextButton").click()
                            found = True
                            browser.find_element_by_name("nextButton").click()
                            break
                    except:
                        pass
                    browser.back()
        except:
            browser.delete_all_cookies()
            time.sleep(60)

    try:
        send_notification()
    except:
        print("FOUND RDV.")
