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
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("no_table_username"))
        email.send_keys(USERS['USER1'])
        password = self.browser.find_element_by_id("no_table_login_password")
        password.send_keys(USERS['PASSWORD1'])
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)

    @data(('/view_event/2', 'Archived', ''))
    @unpack
    def test_archive(self, urltxt, itemtext, itemdesc):
        self.url = ROOT + urltxt
        self.browser.get(self.url)
        time.sleep(2)

        archive_button = self.browser.find_element_by_id("event_archive")
        archive_button.click()

        # submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
        modal_button = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("modal_archive"))
        modal_button.click()

        # refresh and check for archived status
        self.browser.get(self.url)

        # this is not great as shows up even if form not submitted
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(itemtext, body.text)
