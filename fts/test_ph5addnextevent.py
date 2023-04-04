# These tests are all based on the tutorial at http://killer-web-development.com/

from functional_tests import FunctionalTest, ROOT, USERS
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


@ddt
class AddBasicAction (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "no_table_email"))
        email.send_keys(USERS['USER1'])
        password = self.browser.find_element(By.ID, "no_table_password")
        password.send_keys(USERS['PASSWORD1'])
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(1)

    @data(('/view_event/2', 'Next Event Created', ''))
    @unpack
    def test_question(self, urltxt, itemtext, itemdesc):
        self.url = ROOT + urltxt
        self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        # questiontext = self.browser.find_element_by_name('questiontext')

        # submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
        submit_button = self.browser.find_element(By.ID, "next_event")
        submit_button.click()

        # Lookof for body in questiongrid
        # this is not great as shows up even if form not submitted
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
        self.assertIn(itemtext, body.text)
