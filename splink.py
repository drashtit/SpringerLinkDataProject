from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os

download_folder = "/Users/drashtithummar/PycharmProjects/SpringerLink/SplinkCsvData"  # Update this path

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
# Set download preferences
options.add_experimental_option("prefs", {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)  # Setting up an explicit wait
driver.implicitly_wait(3)
driver.get('https://link.springer.com/search/')

# Handle cookie button if present
try:
    cookie_button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                           '//button[@class="cc-button cc-button--secondary cc-button--contrast cc-banner__button cc-banner__button-accept"]')))
    cookie_button.click()
except TimeoutException:
    print("Cookie button not found or not clickable.")

# Find and click refine button
old_page_link = wait.until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/div/div[1]/div/div/p/a')))
old_page_url = old_page_link.get_attribute('href')
original_tab_handle = driver.current_window_handle

driver.execute_script("window.open('" + old_page_url + "');")
new_tab_handle = [handle for handle in driver.window_handles if handle != original_tab_handle][0]
driver.switch_to.window(new_tab_handle)

preview_only = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="results-only-access-checkbox"]')))
preview_only.click()

# List of keywords
my_keys = ["Speech language therapy", "speech language disorder", "speech sound disorder", "articulation disorder", "speech intervention", "language intervention", "Auditory Discrimination", "Auditory Processing Disorder", "Phonological Awareness", "Phonological Processes", "Auditory Perception","Babbling", "Motor Speech Disorder", "Fluency", "Morpheme","Phonology", "Stuttering", "Language Impairment", "Speech-language Pathologist"]

for keyword in my_keys:
    # Switch back to the original tab to perform new search
    # driver.switch_to.window(original_tab_handle)

    # Clear the search box and search for the new keyword
    search_box = wait.until(EC.visibility_of_element_located((By.XPATH, '//input[@name="query"]')))
    search_box.clear()
    search_box.send_keys(keyword)

    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search"]')))
    search_button.click()

    time.sleep(3)  # Consider replacing with a more reliable wait condition
    download_button = driver.find_element(By.XPATH, '//*[@id="tool-download"]/img')
    download_button.click()
    time.sleep(3)

# Close the WebDriver session
driver.quit()
