import sys
import time
import argparse
sys.path.append("home/herilalaina/Documents/Code/prefecture/")

from splinter import Browser


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
    browser = Browser()

    while not found:
        time.sleep(2)
        try:
            browser.visit(url)
            browser.find_by_name("condition").click()
            browser.find_by_name("nextButton").click()


            while not found:
                for id in porte_list:
                    browser.find_by_id(id).click()

                    try:
                        browser.find_by_name("nextButton").click()
                        if browser.is_text_present('Description de la nature du rendez-vous'):
                            browser.find_by_name("nextButton").click()
                            found = True
                            break
                    except:
                        pass
                    browser.back()
        except:
            browser.cookies.delete()


    # Notification ici
    print("Found RDVVV")
