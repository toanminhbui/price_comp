import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def get_lazada_results(query):
    options = Options()
    options.page_load_strategy = 'none'
    # options.headless = True  # Run Chrome in headless mode, no UI.
    driver = webdriver.Chrome(options=options)

    url = f'https://www.lazada.vn/catalog/?q={query}'
    driver.get(url)

    # Wait for dynamic content to load
    # time.sleep(5)  # Adjust sleep time according to your page loading time
    wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Bm3ON'))  # Adjust based on the new page content
        )
    time.sleep(1)
    driver.execute_script("window.stop();")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('div', class_='Bm3ON')
    results = []

    for item in items[:4]:
        title_tag = item.select_one('a')
        link = title_tag['href'] if title_tag else 'N/A'
        link = link.lstrip('/')
        price_tag = item.select_one('.ooOxS')
        price = price_tag.get_text(strip=True) if price_tag else 'N/A'        
        image_wrapper = item.select_one('.picture-wrapper')
        title = image_wrapper.select_one('img')['alt'] if image_wrapper and image_wrapper.select_one('img') else 'N/A'
        if(title == 'N/A'):
            print("not working")
        print(title)
        image = image_wrapper.select_one('img')['src'] if image_wrapper and image_wrapper.select_one('img') else 'N/A'        
        results.append({'title': title, 'price': price, 'image': image, 'link': link})
    driver.quit()
    return results

def get_shopee_results(query):

    # options.headless = True  # Run Chrome in headless mode, no UI.
    options =  Options()
    options.page_load_strategy = 'none'  # Modify based on your requirement
    options.add_argument("--test-type")
    options.add_argument("--disable-extensions")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("enable-automation")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    url = f'https://shopee.vn/search?keyword={query}'
    driver.get(url)
    wait = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'shopee-searchbar'))  # Adjust based on the new page content
        )
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    items = soup.find_all('div', class_='shopee-search-item-result__item')
    results = []
    for item in items[:4]:
        title_tag = item.select_one('.contents')
        title = item.select_one('[class~=line-clamp-2][class~=break-words][class~=min-h-[2.5rem]][class~=text-sm]')
        link = title_tag['href'] if title_tag else 'N/A'
        price = item.select_one('text-base/5 truncate')
        image = title_tag.select_one('img')['src'] if title_tag and title_tag.select_one('img') else 'N/A'    
        results.append({'title': title, 'price': price, 'image': image, 'link': link})
    
    driver.quit()
    return results

def get_dienmaycholon_results(query):
    url = f'https://www.dienmaycholon.vn/ket-qua?key={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.select('.product-item')
    results = []

    for item in items[:4]:
        title = item.select_one('.product-name a').get_text() if item.select_one('.product-name a') else 'N/A'
        link = 'https://www.dienmaycholon.vn' + item.select_one('.product-name a')['href'] if item.select_one('.product-name a') else 'N/A'
        price = item.select_one('.price').get_text() if item.select_one('.price') else 'N/A'
        image = item.select_one('.product-img img')['data-src'] if item.select_one('.product-img img') else 'N/A'
        results.append({'title': title, 'price': price, 'image': image, 'link': link})
    return results

def get_alibaba_results(query):
    url = f'https://www.alibaba.com/trade/search?SearchText={query}'
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(3)  # Wait for page to load
    items = driver.find_elements(By.CSS_SELECTOR, '.J-offer-wrapper')
    results = []

    for item in items[:5]:
        title = item.find_element(By.CSS_SELECTOR, '.elements-title-normal').text
        price = item.find_element(By.CSS_SELECTOR, '.elements-offer-price-normal__price').text
        image = item.find_element(By.CSS_SELECTOR, '.seb-img-switcher__imgs img').get_attribute('src')
        link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        results.append({'title': title, 'price': price, 'image': image, 'link': link})
    driver.quit()
    return results

def main():
    query = input("Enter your search query: ")
    results = {
        # 'Lazada': get_lazada_results(query),
        'Shopee': get_shopee_results(query),
        # 'Dien May Cho Lon': get_dienmaycholon_results(query),
        # 'Alibaba': get_alibaba_results(query)
    }

    for site, items in results.items():
        print(f'\nResults from {site}:')
        for item in items:
            print(f"Title: {item['title']}")
            print(f"Price: {item['price']}")
            print(f"Image: {item['image']}")
            print(f"Link: {item['link']}")
            print('-' * 40)

if __name__ == '__main__':
    main()
