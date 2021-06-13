# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS, CACHETIME
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

@ddt
class AddBasicQuestion (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        get_browser = self.browser.get(self.url)

    @data((USERS['USER2'], USERS['PASSWORD2'], 'User 2 Ph2 Quest', 'Yes', 'No', 'Single'),
          (USERS['USER3'], USERS['PASSWORD3'], 'User 3 Ph2 Quest', 'Yes', 'No', 'Single'),
          (USERS['USER4'], USERS['PASSWORD4'], 'User 4 Ph2 Quest', 'Yes', 'No', 'Single'),
          (USERS['USER5'], USERS['PASSWORD5'], 'User 5 Ph2 Quest', 'Yes', 'No', 'Single'))
    @unpack
    def test_question(self, user, passwd, question, answer1, answer2, resolvemethod):
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("signin"))
        email.send_keys(user)
        password = self.browser.find_element_by_id("signpass")
        password.send_keys(passwd)
        # submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button = self.browser.find_element_by_id("login")
        submit_button.click()
        time.sleep(1)

        self.url = ROOT + '/new_question/0/quest'
        get_browser = self.browser.get(self.url)
        time.sleep(1)

        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        # questiontext = self.browser.find_element_by_name('questiontext')
        itemtext = question
        questiontext = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element_by_id('question_questiontext'))
        questiontext.send_keys(itemtext)

        ans1 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("question_answer1"))
        ans1.send_keys(answer1)

        # ans2 = self.browser.find_element_by_name('ans2')
        ans2 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("question_answer2"))
        ans2.send_keys(answer2)

        resmethod = WebDriverWait(self, 10).until(lambda
                                                      self: self.browser.find_element_by_id("question_resolvemethod"))
        resmethod.send_keys(resolvemethod)

        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)

        # Lookof for body in questiongrid
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(itemtext, body.text)

        # TODO - Need to logout here
        time.sleep(CACHETIME)
