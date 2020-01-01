import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse

next_since_parameter_values = ["0"]  # temporary dynamic variable for the 'next since' parameter
urls = []                            # temporary dynamic massive variable for pagination URLs

    # By this method we get all 'next since' values from API paginations
def get_next_since_values_from_kb_json():
    for next_since_parameter_value in next_since_parameter_values:
        kb_api_base_url = "https://api.figleafapp.com/api/v1/public/kb?since=" + str(
            next_since_parameter_value) + "&limit=1000"
        request_to_api = requests.get(kb_api_base_url).json()
        if request_to_api["status"] == "ok":
            next_since_parameter_values.append(request_to_api["next_since"])

    # By this method we form the batch of URLs with all 'next since' values
def form_urls_for_json_dump():
    for next_since_parameter_value in next_since_parameter_values:
        kb_api_url = "https://api.figleafapp.com/api/v1/public/kb?since=" + str(
            next_since_parameter_value) + "&limit=1000"
        urls.append(kb_api_url)

    # By this method we form global json with all data received by URLs and save data to the kb_data.json
def form_full_json_from_api_with_saving_to_file():
    kb_api_endpoint1 = "https://api.figleafapp.com/api/v1/public/kb?since=" + str(
        next_since_parameter_values[0]) + "&limit=1000"
    for next_since_parameter_value in next_since_parameter_values[1:]:
        request_to_api1 = requests.get(kb_api_endpoint1).json()
        kb_next_api_endpont = "https://api.figleafapp.com/api/v1/public/kb?since=" + str(
            next_since_parameter_value) + "&limit=1000"
        next_request_to_api = requests.get(kb_next_api_endpont).json()
        if next_request_to_api["status"] == "ok":
            request_to_api1["items"] += next_request_to_api["items"]
            with open('kb_data.json', 'w') as outfile:
                json.dump(request_to_api1["items"], outfile)

    # By this method we receive data from the kb_data.json
def get_json_from_file():
    with open('kb_data.json', 'r') as file:
        json_data = json.load(file)
    return json_data

    # By this method we get actual domain from the URL opened by browser
def get_domain_from_site_url(actual_url):
    actual_site_domain = urlparse(actual_url).netloc.replace("www.", "")
    return actual_site_domain

    # By this method we prepare mismatching_domains.txt file for records that have domains/URLs mismatching
def set_mismatches_file():
    open("mismatching_domains.txt", "w").close()

    # By this method we prepare titles_more_than_17_symbols.txt for records that have titles with more than 17 symbols
def set_mismatching_titles():
    open("titles_more_than_17_symbols.txt", "w").close()

    # By this method we save IDs with domains/URLs mismatches to the mismatching_domains.txt file
def save_mismatching_domains(actual_url):
    file = open("mismatching_domains.txt", "a+")
    file.write("For id=" + actual_url + "\r\n")

    # By this method we save IDS with titles more than 17 symbols to the titles_more_than_17_symbols.txt file
def save_mismatching_titles(title):
    file = open("titles_more_than_17_symbols.txt", "a+")
    file.write("Record with id=" + title + "\r\n")

    # By this method checking procedure by desktop browser is executed
def check_domain_desktop_browser(knowledgebase_domain, knowledgebase_id):
    driver = webdriver.Chrome()
    try:
        driver.get("http://" + knowledgebase_domain)
        actual_url = driver.current_url
        actual_domain = get_domain_from_site_url(actual_url)
        print("desktop domain " + actual_domain)
        print("kb domain " + knowledgebase_domain)
        if actual_domain == knowledgebase_domain:
            driver.quit()
        else:
            save_mismatching_domains(str(knowledgebase_id) + " desktop URL domain is " + str(
                actual_domain) + ", but in knowledgebase is " + str(knowledgebase_domain))
            driver.quit()
    except:
        save_mismatching_domains(str(knowledgebase_id) + " domain value '" + str(
            knowledgebase_domain) + "' in knowledgebase is invalid for opening in browser")

    # By this method checking procedure by mobile browser is executed
def check_domain_mobile_browser(knowledgebase_domain, knowledgebase_id):
    try:
        user_agent = "user-agent=Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"
        chrome_options = Options()
        chrome_options.add_argument(user_agent)
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://" + knowledgebase_domain)
        actual_url = driver.current_url
        actual_domain = get_domain_from_site_url(actual_url)
        print("mobile domain " + actual_domain)
        print("kb domain " + knowledgebase_domain)
        if actual_domain == knowledgebase_domain:
            driver.quit()
        else:
            save_mismatching_domains(
                str(knowledgebase_id) + " mobile URL domain is " + str(
                    actual_domain) + ", but in knowledgebase is " + str(
                    knowledgebase_domain))
            driver.quit()
    except:
        print(save_mismatching_domains(str(knowledgebase_id) + " domain value '" + str(
            knowledgebase_domain) + "' in knowledgebase is invalid for opening in browser"))

    # By this method checking titles with more than 17 symbols is executed
def check_title(knowledgebase_title, knowledgebase_id):
    if len(knowledgebase_title) > 17:
        save_mismatching_titles(
            str(knowledgebase_id) + " contains title with length " + str(len(knowledgebase_title)) + " symbols")

    # By this method we parse json data, verify all 'title' values by loop
def select_titles_from_json(json_data):
    for json_data[0] in json_data:
        check_title(json_data[0]["title"], json_data[0]["id"])

    # By this method we parse json data, verify all 'domains' values by loop
def select_domains_from_json(json_data):
    for json_data[0] in json_data:
        print(json_data[0]["id"])
        check_domain_desktop_browser(json_data[0]["domains"][0], json_data[0]["id"])
        check_domain_mobile_browser(json_data[0]["domains"][0], json_data[0]["id"])


get_next_since_values_from_kb_json()
form_urls_for_json_dump()
form_full_json_from_api_with_saving_to_file()
set_mismatching_titles()
select_titles_from_json(get_json_from_file())
set_mismatches_file()
select_domains_from_json(get_json_from_file())