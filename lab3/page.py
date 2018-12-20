from lab3.element import BasePageElement
from lab3.locators import MainPageLocators
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    #The locator for search box where search string is entered
    locator = 'q'


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver


class MainPage(BasePage):
    """Home page action methods come here. I.e. Python.org"""

    #Declares a variable that will contain the retrieved text
    def create_task(self, name):
        WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element_by_class_name("new-todo"))
        element = self.driver.find_element_by_class_name("new-todo")
        element.send_keys(name + Keys.ENTER)

    def get_tasks(self):
        tasks = self.driver.find_element_by_class_name("todo-list")
        ret_arr = []
        for t in tasks.find_elements_by_class_name('view'):
            ret_arr.append(t)
        return ret_arr


class SearchResultsPage(BasePage):
    """Search results page action methods come here"""

    def is_results_found(self):
        # Probably should search for this text in the specific page
        # element, but as for now it works fine
        return "No results found." not in self.driver.page_source