import os
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

subject = input("What do you want to search for? ")
max_images = int(input("How many images do you want to download? "))
# Create a folder to store the images
os.makedirs(f'{subject}_images', exist_ok=True)

driver = webdriver.Chrome()
driver.get("https://images.google.com/")

search = driver.find_element(By.NAME, "q")
search.send_keys(subject)
search.send_keys(Keys.RETURN)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'img')))

imgs = driver.find_elements(By.TAG_NAME, 'img')

image_count = 0  # Initialize a counter to track the number of downloaded images
for img in imgs:
    if image_count >= max_images:
        break  # Stop the loop if the maximum number of images is reached

    alt = img.get_attribute("alt")

    if alt and alt.strip() != "":
        img.click()
        time.sleep(0.5)
        targetImg = driver.find_elements(By.XPATH, f'//img[@alt="{alt}"]')

        for t in targetImg:
            src = t.get_attribute("src")

            if src and src.startswith('http') and not src.startswith('https://encrypted-tbn0.gstatic.com'):
                # Increment the counter each time an image is downloaded
                image_count += 1

                # Sanitize the alt text to remove invalid characters
                alt = re.sub(r'[<>:"/\\|?*]', '_', alt)

                response = requests.get(src)

                with open(f'{subject}_images/{alt}.jpg', 'wb') as f:
                    f.write(response.content)

                # Check if the maximum number of images is reached after downloading each image
                if image_count >= max_images:
                    break

driver.quit()
