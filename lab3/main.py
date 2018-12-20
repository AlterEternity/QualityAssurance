import unittest
from selenium import webdriver
from lab3.page import MainPage

class PythonOrgSearch(unittest.TestCase):
    """A sample test class to show how page object works"""

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://todomvc.com/examples/angularjs/#/")

    def test_create_task_task_creates(self):
        test_page = MainPage(self.driver)
        test_page.create_task("New_task")
        assert len(test_page.get_tasks()) == 1

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()