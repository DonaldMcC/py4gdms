# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait


@ddt
class AddBasicAction (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        get_browser = self.browser.get(self.url)
        time.sleep(2)

        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("none_username"))
        email.send_keys(USERS['USER2'])
        password = self.browser.find_element_by_id("none_login_password")
        password.send_keys(USERS['PASSWORD2'])
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)


    @data(('/new_question/0/action', 'Lets get this done'), ('/new_question/0/issue', 'The world is under-achieving'))
    @unpack
    def test_question(self, urltxt, itemtext):
        self.url = ROOT + urltxt
        get_browser = self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        # questiontext = self.browser.find_element_by_name('questiontext')
        questiontext = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_name('questiontext'))
        questiontext.send_keys(itemtext)

        # submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)

        # Lookof for body in questiongrid
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(itemtext, body.text)

