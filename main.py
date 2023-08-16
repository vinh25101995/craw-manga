# This is a sample Python script.
import base64

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from io import BytesIO
from PIL import Image
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
def selenium_craw():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_argument("--disable-web-security")
    service = Service('F:/Setup/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://cuutruyen.net/mangas/446/chapters/25729")
    time.sleep(5)
    driver.implicitly_wait(5)
    # classic_ui = driver.find_element(By.XPATH, '//*[contains(text(), " Classic UI ")]')
    # classic_ui.click()
    # time.sleep(1)
    btn = driver.find_element(By.XPATH, '//button[text()="Xác nhận"]')
    btn.click()
    driver.implicitly_wait(5)
    time.sleep(5)
    canvas = WebDriverWait(driver, 180).until(
        EC.presence_of_element_located((By.TAG_NAME, "canvas"))
    )
    # Kiểm tra trạng thái của canvas
    is_image_loaded = driver.execute_script(
        "return arguments[0].complete && typeof arguments[0].naturalWidth !== 'undefined' && "
        "arguments[0].naturalWidth > 0",
        canvas
    )
    images = driver.find_elements(By.TAG_NAME, "canvas")
    if is_image_loaded:
        print("Ảnh đã tải xong.")
    else:
        print("Ảnh chưa tải xong.")
    i = 0
    size = len(images)
    while i < size - 1:
        image = images[i]
        image_data = driver.execute_script("return arguments[0].toDataURL()", image)
        if image_data:
            i = i + 1
            image_data = image_data[22:]
            try:
                decoded_data = base64.b64decode(image_data)
            except base64.binascii.Error:
                print("Invalid base64 data")
                # Handle the error or return accordingly

            # Verify image dimensions
            try:
                image = Image.open(BytesIO(decoded_data))
                width, height = image.size
                if width == 0 or height == 0:
                    print("Invalid image dimensions")
                else:
                    image_extension = image.format
                    print("Image[", str(i), "] dimensions:", width, "x", height, "x Extension:", image_extension)
                    # with open(str(i) + ".png", 'wb') as f:
                    #     f.write(decoded_data)
                    image.save(str(i) + ".png")
            except (OSError, IOError):
                print("Unable to open the Image[", str(i), "]")
            body_element = driver.find_element(By.TAG_NAME, "body")
            body_element.send_keys(Keys.ARROW_LEFT)
            time.sleep(0.6)
            # driver.implicitly_wait(5)
            # images = driver.find_elements(By.TAG_NAME, "canvas")

    # driver.quit()


def beatisoup_craw():
    # Send a GET request to the webpage
    url = "https://cuutruyen.net/mangas/446/chapters/23993"
    response = requests.get(url)

    # Create a BeautifulSoup object from the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the canvas elements
    canvas_elements = soup.find_all("canvas")

    i = 0
    total_height = 0

    # Loop through the canvas elements
    for canvas in canvas_elements:
        # Get the base64-encoded image data
        image_data = canvas["data-url"]
        if image_data:
            i += 1
            image_data = image_data[22:]
            try:
                # Decode the base64 data
                decoded_data = base64.b64decode(image_data)
            except base64.binascii.Error:
                print("Invalid base64 data")
                continue

            try:
                # Open the image using PIL
                image = Image.open(BytesIO(decoded_data))
                width, height = image.size
                if width == 0 or height == 0:
                    print("Invalid image dimensions")
                else:
                    image_extension = image.format.lower()
                    print("Image[", str(i), "] dimensions:", width, "x", height, "x Extension:", image_extension)
                    # Save the image to a file
                    image.save(str(i) + ".png")
                    total_height += height
            except (OSError, IOError):
                print("Unable to open the Image[", str(i), "]")

    print("Total images:", i)


if __name__ == '__main__':
    selenium_craw()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
