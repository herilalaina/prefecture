import sys, os
import time
import random
import argparse
from selenium import webdriver
from twilio.rest import Client
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy

# req_proxy = RequestProxy()  # you may get different number of proxy when  you run this at each time
# proxies = req_proxy.get_proxy_list()  # this will create proxy list

sys.path.append(os.sep.join([os.environ.get("ROOT_APP_PREFECTURE")]))


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
    page_ok = ("naturalisation" in _browser.find_element_by_tag_name('html').text.lower())
    c = 0
    while (not page_ok) and (c < 10):
        _browser.refresh()
        page_ok = ("naturalisation" in _browser.find_element_by_tag_name('html').text.lower())
        c += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='RDV Prefecture')
    parser.add_argument(
        '--type', '-t',
        help='Type RDV (NAT, DEC)',
        type=str,
        choices=["NAT", "DEC"],
        required=True
    )
    args = parser.parse_args()

    browser = webdriver.Firefox()
    found = False
    if args.type == "NAT":
        url = 'http://www.essonne.gouv.fr/booking/create/23014/'
        porte_list = ["planning23018", "planning23198", "planning23199", "planning23200", "planning23201"]
    elif args.type == "DEC":
        url = 'http://www.essonne.gouv.fr/booking/create/30986/'
        porte_list = ["planning30987", "planning30988"]
    else:
        raise Exception("Error type RDV.")

    while not found:
        try:
            browser.get(url)
            browser.find_element_by_id("condition").click()
            element = browser.find_element_by_name("nextButton")
            browser.execute_script("arguments[0].click();", element)
            reload(browser)
            while not found:
                random.shuffle(porte_list)
                for id in porte_list:
                    time.sleep(4)
                    browser.find_element_by_id(id).click()
                    reload(browser)
                    try:
                        browser.find_element_by_name("nextButton").click()
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

    # Notification ici
    send_notification()
