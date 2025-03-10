import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DivanRu:
    def __init__(self,
                 driver,
                 base_url,
                 butt_path='.//div[@id="root"]/header/div[2]//button',
                 butt_path_hidden='.//div[@id="root"]/header/div/div/button',
                 category_hidden='.//div[@data-testid="page-index"]/div[2]//a[contains(@href,"/category/") and not(contains(@href,"promo-"))]',
                 category_path='.//div[@id="root"]/div/div[2]/div/div/div/div/div/a'):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(self.driver, 10)
        self.categories = []
        self.butt_path = butt_path
        self.butt_path_hidden = butt_path_hidden
        self.category_hidden = category_hidden
        self.category_path = category_path

    def get_category(self):
        self.driver.get(self.base_url)
        buttons = button = self.driver.find_elements(By.XPATH,self.butt_path)
        # body_style = self.driver.find_element(By.TAG_NAME, "body").get_attribute("style")
        if len(buttons) ==0:
            butt_menu = self.driver.find_element(By.XPATH,self.butt_path_hidden)
            butt_menu.click()
            # time.sleep(1)
            # butt_menu = self.driver.find_element(By.XPATH,self.category_hidden)
            # butt_menu.click()
            self.categories = [ [category.get_attribute('href'),category.find_element(By.XPATH,'./div[2]').text] for category in self.driver.find_elements(By.XPATH,self.category_hidden)]

            # butt_menu.click()
        else:
            #button = self.driver.find_elements(By.XPATH,self.butt_path)
            buttons[0].click()
            self.categories = [ [category.get_attribute('href'),category.find_element(By.XPATH,'.//div/div' ).text] for category in self.driver.find_elements(By.XPATH, self.category_path) if category]

