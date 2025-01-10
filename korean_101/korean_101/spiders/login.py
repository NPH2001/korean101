import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
import json
from dotenv import load_dotenv
import os
import time


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["koreanclass101.com"]
    start_urls = ["https://www.koreanclass101.com"]

    load_dotenv()

    username = os.getenv("USER_NAME")
    password = os.getenv("PASS_WORD")

    def start_requests(self):
        url = "https://www.koreanclass101.com/index.php"
        yield SeleniumRequest(
            url=url,
            callback=self.login,
            screenshot=True,
            wait_time=30
        )

    def login(self, response):
        driver = response.request.meta['driver']

        btn_login = driver.find_element(
            By.XPATH, "//button[contains(@class, 'dashbar-a__block--sign-in-button') and text()='Sign In']")
        btn_login.click()

        username_input = driver.find_element(By.ID, 'r101-sign-in-login')
        password_input = driver.find_element(By.ID, 'r101-sign-in-password')

        username_input.send_keys(self.username)
        time.sleep(2)
        password_input.send_keys(self.password)

        driver.find_element(
            By.XPATH, "//div[@class='r101-sign-in--a__form-btn-wrap']/button[@type='submit' and text()='Sign In']").click()

        time.sleep(6)
        cookies = driver.get_cookies()
        with open('cookies.json', 'w') as file:
            json.dump(cookies, file)

        print("Cookies saved successfully.")

        driver.quit()
