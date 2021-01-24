# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS, CACHETIME
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


class AddBasicQuestion (FunctionalTest):

    def setUp(self):     
        self.url = ROOT + '/auth/login'
        get_browser = self.browser.get(self.url)
        time.sleep(2)
        mailstring = USERS['USER2']+'@user.com'

        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("none_username"))
        email.send_keys(USERS['USER2'])
        password = self.browser.find_element_by_id("none_login_password")
        password.send_keys(USERS['PASSWORD2'])
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")

        submit_button.click()
        time.sleep(1)

        self.url = ROOT + '/new_question/0/quest'
        get_browser = self.browser.get(self.url)
        time.sleep(1)


    def test_question(self):
        time.sleep(2) # still getting blank category for some reason but not if loaded manually
        # questiontext = self.browser.find_element_by_name('questiontext')
        questiontext = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id('question_questiontext'))
        questiontext.send_keys("Selenium to be or not to be")

        # ans1 = self.browser.find_element_by_name('ans1')
        ans1 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("question_answer1"))
        ans1.send_keys("be")
        ans1.send_keys(Keys.RETURN)

        #ans2 = self.browser.find_element_by_name('ans2')
        ans2 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_xpath("(//input[@id='question_answers'])[2]"))
        ans2.send_keys("not to be")

        submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
        submit_button.click()
        time.sleep(1)
  
        #welcome_message = self.browser.find_element_by_css_selector(".w2p_flash")
        #self.assertIn('Details Submitted', welcome_message.text)

        time.sleep(CACHETIME)
