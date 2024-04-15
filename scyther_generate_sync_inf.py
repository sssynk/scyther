# scyther-generator by synk

challenge = ""
email_domain = ""

from selenium import webdriver
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.webdriver.support.wait import WebDriverWait
from threading import Thread, Timer
from time import sleep
from signal import pause
import webhook_listener
import json
import string
import random
import requests

processed_emails = []

def check_for_email(email):
    while True:
        # get request /queue
        r = requests.get('http://localhost:8090/queue')
        r = r.json()

        # remove emails and codes that have already been processed (email and code must match)
        for processed_email in processed_emails:
            if processed_email['email'] in r and processed_email['code'] == r[processed_email['email']]:
                del r[processed_email['email']]

        if email in r:
            processed_emails.append({'email': email, 'code': r[email]})
            return r[email]
        sleep(1)

def log(data):
    print("[scyther-info] " + data)

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))




def generate_account():
    try:
        global currentPort
        # load proxies from proxies.txt
        proxies = []
        with open("proxies.txt") as f:
            # each proxy is IP:PORT on newline
            for line in f:
                proxies.append(line.strip())

        # make/open file for recently used proxies
        recently_used_proxies = []
        #try:
           # with open("recently_used_proxies.txt") as f:
                #for line in f:
                    #recently_used_proxies.append(line.strip())
                    #except:
            #with open("recently_used_proxies.txt", "w") as f:
                #pass

        # remove recently used proxies from proxies list
        #for proxy in recently_used_proxies:
            #if proxy in proxies:
                #proxies.remove(proxy)

        # if no proxies left, empty recently used proxies and start again
        #if len(proxies) == 0:
            #with open("recently_used_proxies.txt", "w") as f:
                #pass
            #with open("proxies.txt") as f:
                #for line in f:
                    #proxies.append(line.strip())

        # choose random proxy
        proxy = random.choice(proxies)

        # add proxy to recently used proxies
        #recently_used_proxies.append(proxy)

        # write recently used proxies to file
        #with open("recently_used_proxies.txt", "w") as f:
            #for proxy in recently_used_proxies:
                #f.write(proxy + "\n")

        log("Using proxy "+proxy)

        screenName = id_generator(size=4)
        accountName = id_generator(size=8)
        accountPassword = id_generator(size=28, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation) + "000"

        # remove all colons from password
        accountPassword = accountPassword.replace(":", "")

        log("Generating account with name scyther"+accountName+" and password "+accountPassword+"...")

        # prepare proxy

        options = uc.ChromeOptions()
        options.add_argument(f'--proxy-server='+proxy)
        options.add_argument('--lang=en')

        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option('useAutomationExtension', False)
        #options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        driver = uc.Chrome(options=options, headless=True, user_multi_procs=True, browser_executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        #driver = webdriver.Chrome(options=options)
        #stealth(driver,
        #        languages=["en-US", "en"],
        #        vendor="Google Inc.",
        #        platform="Win32",
        #        webgl_vendor="Intel Inc.",
        #        renderer="Intel Iris OpenGL Engine",
        #        fix_hairline=True,
        #        )

        driver.get("https://join.pokemon.com/")

        title = driver.title

        WebDriverWait(driver, 60).until(lambda driver: driver.find_element(by=By.ID, value="ageGateSubmit"))

        #sleep(0.5)

        country = driver.find_element(by=By.ID, value="country-select")
        year = driver.find_element(by=By.ID, value="year-select")
        month = driver.find_element(by=By.ID, value="month-select")
        day = driver.find_element(by=By.ID, value="day-select")
        nextButton = driver.find_element(by=By.ID, value="ageGateSubmit")

        country.send_keys("United States")
        year.send_keys("1990")
        month.send_keys("January")
        day.send_keys("12")

        #sleep(0.5)

        nextButton.click()

        #sleep(0.5)

        driver.find_element("xpath","//button[contains(text(), 'Yes, it is')]").click()

        #sleep(0.5)

        email = driver.find_element(by=By.ID, value="email-text-input")
        confirm = driver.find_element(by=By.ID, value="confirm-text-input")

        email.send_keys(accountName+"@"+email_domain)
        confirm.send_keys(accountName+"@"+email_domain)

        #sleep(0.5)

        driver.find_element("xpath","//button[contains(text(), 'Continue')]").click()

        log("Bypassing Imperva Bot Detection...")
        # wait until the text "Please review and accept Terms of Use" is visible

        try:
            WebDriverWait(driver, 15).until(lambda driver: driver.find_element("xpath","//div[contains(text(), 'Please review and accept Terms of Use')]"))
        except:
            log("Failed to bypass Imperva Bot Detection. Aborting and retrying...")
            driver.quit()
            generate_account()
            return

        log("Bypassed!")

        #sleep(0.5)

        driver.find_element("xpath","//button[contains(text(), 'Accept')]").click()

        #sleep(0.5)

        driver.find_element("xpath","//button[contains(text(), 'Accept')]").click()

        #sleep(0.5)

        usernameInput = driver.find_element(by=By.ID, value="screen_name-text-input")

        usernameInput.send_keys("scyther"+screenName)

        #sleep(0.5)

        driver.find_element("xpath","//button[contains(text(), 'Continue')]").click()

        #sleep(0.5)

        WebDriverWait(driver, 60).until(lambda driver: driver.find_element("xpath","//h1[contains(text(), 'Enter the username and password')]"))

        usernameInput = driver.find_element(by=By.ID, value="username-text-input")
        paswordInput = driver.find_element(by=By.ID, value="password-text-input")

        usernameInput.send_keys("scyther"+accountName)
        paswordInput.send_keys(accountPassword)

        #sleep(0.5)

        driver.find_element("xpath","//button[contains(text(), 'Create Account')]").click()

        #sleep(0.5)

        WebDriverWait(driver, 60).until(lambda driver: driver.find_element("xpath","//button[contains(text(), 'Yes, it is')]"))

        driver.find_element("xpath","//button[contains(text(), 'Yes, it is')]").click()

        log("Waiting for code...")

        code = check_for_email(accountName+"@"+email_domain)

        log("Verifying code "+code+" for PTC...")

        codeinput = driver.find_element(by=By.ID, value="code-text-input")
        codeinput.send_keys(code)

        driver.find_element("xpath","//button[contains(text(), 'Continue')]").click()

        log("Verifying code with PoGo servers...")

        log("Verifying "+accountName+" (PoGo)...")

        driver.get("https://join.pokemon.com/?jump_activate=activation&username=scyther"+accountName+"&challenge="+challenge)

        WebDriverWait(driver, 60).until(lambda driver: driver.find_element("xpath","//button[contains(text(), 'Continue')]"))

        codeinput = driver.find_element(by=By.ID, value="code-text-input")
        codeinput.send_keys(code)

        driver.find_element("xpath","//button[contains(text(), 'Continue')]").click()

        log("Waiting for verification from server...")

        try:
            WebDriverWait(driver, 15).until(lambda driver: driver.find_element("xpath","//h1[contains(text(), 'Success')]"))
        except:
            log("Failed to verify account. Aborting and retrying...")
            driver.quit()
            generate_account()
            return

        log("Account created successfully (passed all verifications)")

        log("Account created! scyther"+accountName+" with password "+accountPassword+" and email "+accountName+"@"+email_domain)

        with open("accounts.txt", "a") as f:
            f.write("scyther"+accountName+":"+accountPassword+"\n")

        driver.quit()
    except:
        log("Failed to create account. Retrying...")
        generate_account()
        return


# sync generation

print("scyther PTC account generator")
numAccounts = 50000

for i in range(numAccounts // 4):
    t1 = Thread(target=generate_account)
    t2 = Thread(target=generate_account)
    t3 = Thread(target=generate_account)
    t1.start()
    sleep(0.25)
    t2.start()
    sleep(0.25)
    t3.start()
    sleep(0.25)
    generate_account()
    t1.join()
    t2.join()
    t3.join()


log("Done")
