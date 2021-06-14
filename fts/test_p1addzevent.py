# These tests are all based on the tutorial at http://killer-web-development.com/

from functional_tests import FunctionalTest, ROOT, USERS
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait


@ddt
class AddBasicAction (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("signin"))
        email.send_keys(USERS['USER1'])
        password = self.browser.find_element_by_id("signpass")
        password.send_keys(USERS['PASSWORD1'])
        #submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button = self.browser.find_element_by_id("login")
        submit_button.click()
        time.sleep(1)

    @data(('/new_event', 'P1Test', 'Phase 1 test event'), ('/new_event', 'P1Test2', 'Phase 1 test event2'))
    @unpack
    def test_question(self, urltxt, itemtext, itemdesc):
        self.url = ROOT + urltxt
        get_browser = self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        # questiontext = self.browser.find_element_by_name('questiontext')
        questiontext = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_name('event_name'))
        questiontext.send_keys(itemtext)

        questiontext = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_name('description'))
        questiontext.send_keys(itemdesc)

        # submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)

        # Lookof for body in questiongrid
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(itemtext, body.text)
