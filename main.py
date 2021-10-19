import sys
import time
import random
import argparse
sys.path.append("home/herilalaina/Documents/Code/prefecture/")

from splinter import Browser


def reload(_browser):
    page_ok = ("naturalisation" in _browser.html.lower())
    c = 0

    while (not page_ok) and (c < 10):
        _browser.reload()
        page_ok = ("naturalisation" in _browser.html.lower())
        c += 1

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='RDV Prefecture')
    parser.add_argument(
        '--type', '-t',
        help='Type RDV (NAT, DEC)',
        type=str,
        choices=["NAT", "DEC"],
        required=True
    )
    args = parser.parse_args()

    if args.type == "NAT":
        url = 'http://www.essonne.gouv.fr/booking/create/23014/'
        porte_list = ["planning23018", "planning23198", "planning23199", "planning23200", "planning23201"]
    elif args.type == "DEC":
        url = 'http://www.essonne.gouv.fr/booking/create/30986/'
        porte_list = ["planning30987", "planning30988"]
    else:
        raise Exception("Error type RDV.")

    found = False
    browser = Browser(timeout=130)

    while not found:
        try:
            browser.visit(url)
            browser.find_by_name("condition").click()
            browser.find_by_name("nextButton").click()
            reload(browser)


            while not found:
                random.shuffle(porte_list)
                for id in porte_list:
                    time.sleep(40)
                    browser.find_by_id(id).click()
                    reload(browser)

                    try:
                        browser.find_by_name("nextButton").click()
                        if browser.is_text_present('Description de la nature du rendez-vous'):
                            browser.find_by_name("nextButton").click()
                            found = True
                            browser.find_by_name("nextButton").click()
                            break
                    except:
                        pass
                    browser.back()
        except:
            browser.cookies.delete()
            time.sleep(60)


    # Notification ici
    print("Found RDVVV")
