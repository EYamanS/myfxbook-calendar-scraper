import requests
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import json

def main():
    
    run_data = json.load(open("config.json","r"))
    login_url = run_data.get("login_url")
    search_url = run_data.get("search_url")
    filename = run_data.get("output_file_name")
    email = run_data.get("email")
    password = run_data.get("password")

    if (login_url == "" or search_url == "" or email == "" or password == "" or filename == ""):
        print("Missing values in config.json.\nMake sure you've set them as specified")
        return None
    
    requests_data = try_requests(search_url)    

    if (requests_data["did_ran"]):
        print("Classic request executed successfully. Writing content...")
        writexmlcontent(filename,requests_data["content"])
    else:
        print("\nClassic request failed. Running selenium...")
        update_cookies(login_url,email,password,search_url)
        
        print("\nUpdated cookies. Re-running requests..")
        requests_data = try_requests(search_url)

        if (requests_data["did_ran"]):
            print("Classic request executed successfully. Writing content...")
            writexmlcontent(filename,requests_data["content"])
        else:
            print("\nNew cookies also failed :(\nPlease contact me. eyamansivrikaya@outlook.com\n")
            return None

def update_cookies(login_url,email,password,needed_url):
    
    options = webdriver.ChromeOptions()

    ser = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=ser)
    driver.get(login_url)

    try:
        WebDriverWait(driver, 1.5).until(EC.presence_of_element_located((By.ID,"YAMAN")))
    except:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginEmail"))).send_keys(email)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "loginPassword"))).send_keys(password)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "login-btn"))).click()
        WebDriverWait(driver,5).until(EC.visibility_of_element_located((By.CLASS_NAME,"portlet-title")))
        driver.get(needed_url)


        latest_cookie_dict = {}
        for cookie in driver.get_cookies():
            if ("fxsession" not in cookie.values()):
                continue
            else:
                for key in cookie.keys():
                    latest_cookie_dict[key] = str(cookie[key])
        
        for request in driver.requests:
            if (request.url != "https://www.myfxbook.com/calendar_statement.xml?&start=&end=&filter="):
                continue
            else:
                last_header_cookie = request.headers                

    with open("config.json",'r') as ch:
        config = json.load(ch)
        for hdr in last_header_cookie:
            config["latest_header_cookie"][hdr] = last_header_cookie[hdr]
        config["latest_cookies"] = latest_cookie_dict

    with open("config.json",'w') as cf:
        json.dump(config,cf,indent=3)



def try_requests(base_url):
    conf = json.load(open("config.json","r"))
    cookie = conf['latest_cookies']
    response = requests.get(base_url,headers=conf["latest_header_cookie"],cookies=cookie)

    if (response.content != b''):
        return {"did_ran": True, "content": response.content}
    else:
        return {"did_ran": False}


def writexmlcontent(filename,content,binary=True):
    if (binary):
        with open(filename,"wb") as fh:
            fh.write(content)
    else:
        with open(filename,"w") as fh:
            fh.write(content)
    
    print("Content written to: ", filename, "\nHave a great day :)")
main()


# Made by Emir Yaman Sivrikaya.