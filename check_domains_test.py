import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

def get_json_from_api():
    kb_api_endpoint1 = "https://api.figleafapp.com/api/v1/public/kb?since=0&limit=1000"
    kb_api_endpoint2 = "https://api.figleafapp.com/api/v1/public/kb?since=1561444788218314&limit=1000"
    request_to_api1 = requests.get(kb_api_endpoint1).json()
    request_to_api2 = requests.get(kb_api_endpoint2).json()
    request_to_api1["items"] += request_to_api2["items"]
    with open('kb_data.json', 'w') as outfile:
        json.dump(request_to_api1["items"], outfile)

def get_json_from_file():
    with open('kb_data.json', 'r') as file:
        json_data = json.load(file)
    return json_data

def get_domain_from_url(actual_url):
    actual_site_domain = urlparse(actual_url).netloc.replace("www.", "")
    return actual_site_domain

def set_mismatches_file():
    open("mismatching_domains.txt", "w").close()

def save_mismatching_domains(actual_url):
    file = open("mismatching_domains.txt", "a+")
    file.write("For id=" + actual_url + "\r\n")

def check_domain_desktop_browser(knowledgebase_domain, knowledgebase_id):
    driver = webdriver.Chrome()
    try:
        driver.get("http://" + knowledgebase_domain)
        actual_url = driver.current_url
        actual_domain = get_domain_from_url(actual_url)
        print("desktop domain " + actual_domain)
        print("kb domain " + knowledgebase_domain)
        if actual_domain == knowledgebase_domain:
            driver.quit()
        else:
            save_mismatching_domains(str(knowledgebase_id) + " desktop URL domain is " + str(actual_domain) + ", but in knowledgebase is " + str(knowledgebase_domain))
            driver.quit()
    except:
        save_mismatching_domains(str(knowledgebase_id) + " domain value '" + str(knowledgebase_domain) + "' in knowledgebase is invalid for opening in browser")

def check_domain_mobile_browser(knowledgebase_domain, knowledgebase_id):
    try:
        user_agent = "user-agent=Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
        chrome_options = Options()
        chrome_options.add_argument(user_agent)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get("http://" + knowledgebase_domain)
        actual_url = driver.current_url
        actual_domain = get_domain_from_url(actual_url)
        print("mobile domain " + actual_domain)
        print("kb domain " + knowledgebase_domain)
        if actual_domain == knowledgebase_domain:
            driver.quit()
        else:
            save_mismatching_domains(
                str(knowledgebase_id) + " mobile URL domain is " + str(actual_domain) + ", but in knowledgebase is " + str(
                    knowledgebase_domain))
            driver.quit()
    except:
        print(save_mismatching_domains(str(knowledgebase_id) + " domain value '" + str(knowledgebase_domain) + "' in knowledgebase is invalid for opening in browser"))

def select_domains_from_json(json_data):
    for json_data[0] in json_data:
        check_domain_desktop_browser(json_data[0]["domains"][0], json_data[0]["id"])
        check_domain_mobile_browser(json_data[0]["domains"][0], json_data[0]["id"])

#get_json_from_api()
#set_mismatches_file()
select_domains_from_json(get_json_from_file())



