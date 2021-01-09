import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import urllib.parse


## Configuration ###################################################################################
# PROXY = "127.0.0.1:1080"
PROXY = False

# Init
if PROXY:
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy": PROXY,
        "ftpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
    }


## Functions #######################################################################################
def translate(text: str, lang_tgt: str='ZH', lang_src: str = 'EN', detect: bool=False)-> str:
    if detect:
        lang_src = 'auto'
    text = urllib.parse.quote(text)
    load_url = f'https://www.deepl.com/en/translator#{lang_src}/{lang_tgt}/{text}'
    result = "API Error"
    d = open_driver(load_url)
    while 1:
        selector = "#dl_translator > div.lmt__text > div.lmt__sides_container > div.lmt__side_container.lmt__side_container--target > div.lmt__textarea_container.halfViewHeight > div.lmt__translations_as_text > p.lmt__translations_as_text__item.lmt__translations_as_text__main_translation > button.lmt__translations_as_text__text_btn"
        try:
            result = d.find_element_by_css_selector(selector).get_attribute(
                "textContent")
            if result != "":
                break
            time.sleep(0.3)
        except StaleElementReferenceException:
            print(f"Element not found: {selector.split('')[-1]}")
    return result, d


def open_driver(url: str) -> webdriver.Chrome:
    prefs = {
        'profile.managed_default_content_settings.images': 2,
        'permissions.default.stylesheet': 2,
    }
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option('prefs', prefs)
    d = webdriver.Chrome('./webdriver/chromedriver', options=chrome_options)
    d.get(url)
    return (d)


def quit_driver(d: webdriver.Chrome) -> None:
    d.close()
    d.quit()


## Default function ################################################################################
if __name__ =="__main__":
    time_start = time.time()
    try:
        str_to_translate = '''Translation works correctly'''
        result = translate(str_to_translate, lang_tgt='EN', detect=True)
        time_end = time.time()
        quit_driver(result[1])
        print(result[0], '(Time', time_end - time_start, 'seconds.)')
    except KeyboardInterrupt as k:
        time_end = time.time()
        print('\nKey pressed to interrupt...', '(Time', time_end - time_start,
              'seconds.)')
