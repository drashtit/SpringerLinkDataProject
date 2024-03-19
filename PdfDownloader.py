from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Specify the path to your desired download folder
download_folder = "/Users/drashtithummar/PycharmProjects/SpringerLink/SpeechLanguagePathologist"

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
# Set custom download preferences
options.add_experimental_option('prefs', {
    "download.default_directory": download_folder,  # Change default directory for downloads
    "download.prompt_for_download": False,  # Disable download prompt
    "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)  # Setting up an explicit wait
driver.implicitly_wait(3)
driver.get('https://link.springer.com/search/')

try:
    cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                           '//button[@class="cc-button cc-button--secondary cc-button--contrast cc-banner__button cc-banner__button-accept"]')))
    cookie_button.click()
except TimeoutException:
    print("Cookie button not found or not clickable.")

old_page_link = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/div/div/p/a')))
old_page_url = old_page_link.get_attribute('href')
original_tab_handle = driver.current_window_handle

driver.execute_script("window.open('" + old_page_url + "');")
new_tab_handle = [handle for handle in driver.window_handles if handle != original_tab_handle][0]
driver.switch_to.window(new_tab_handle)

preview_only = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="results-only-access-checkbox"]')))
preview_only.click()
type_article_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@class="facet-title" and text()="Article"]')))
type_article_btn.click()

# my_keys = ["speech language therapy", "speech language disorder", "speech sound disorder", "articulation disorder", "speech intervention", "language intervention", "Auditory Discrimination", "Auditory Processing Disorder", "Phonological Awareness", "Phonological Processes", "Auditory Perception","Babbling", "Motor Speech Disorder", "Fluency", "Morpheme","Phonology", "Stuttering", "Language Impairment", "Speech-language Pathologist"]
my_keys = ["Speech-language Pathologist"]

for keyword in my_keys:
    search_box = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="query"]')))
    search_box.clear()
    search_box.send_keys(keyword)
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]')))
    search_button.click()

    while True:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//ol[@class="content-item-list"]')))
        article_list = driver.find_elements(By.XPATH, '//ol[@class="content-item-list"]/li')

        for article in article_list:
            original_window = driver.current_window_handle
            try:
                article_link = article.find_element(By.XPATH, './/a[@class="title"]')  # Adjusted to './/a[@class="title"]' for a more reliable match
                link = article_link.get_attribute('href')
                # print(link)

                # Open the article link in a new window
                driver.execute_script(f"window.open('{link}');")
                new_window = driver.window_handles[-1]
                driver.switch_to.window(new_window)

                download_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="c-pdf-download u-clear-both u-mb-16"]/a')))
                download_button.click()
                time.sleep(3)  # Adjust based on your connection speed and response time

                driver.close()
                driver.switch_to.window(original_window)

            except NoSuchElementException:
                print("Article link not found within article element.")
                driver.switch_to.window(original_window)
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
                driver.switch_to.window(original_window)

        try:
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="next"]')))
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
        except TimeoutException:
            print("No more pages to navigate.")
            break

driver.quit()
