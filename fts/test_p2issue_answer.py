# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS, questiddict
import time
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


@ddt
class AnswerQuestion (FunctionalTest):

    def setUp(self):   
        pass

    @data((USERS['USER2'], USERS['PASSWORD2'], 'Answer recorded'),
          (USERS['USER3'], USERS['PASSWORD3'], 'Answer recorded'),
          (USERS['USER4'], USERS['PASSWORD4'], 'Resolved'))
    @unpack
    def test_answer(self, user, passwd, result):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        qid = questiddict.get('p2issue')

        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("no_table_email"))
        email.send_keys(user)
        password = self.browser.find_element_by_id("no_table_password")
        password.send_keys(passwd)
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)

        self.url = ROOT + '/index/issues/'+str(qid)
        get_browser = self.browser.get(self.url)
        time.sleep(1)
        # self.browser.find_element_by_xpath("(//input[@name='ans'])[2]").click()

        # answer issue
        self.browser.find_element(By.CSS_SELECTOR, "td:nth-child(3) > .is-success").click()

        time.sleep(1)

        # body = self.browser.find_element_by_tag_name('body')
        body = WebDriverWait(self, 10).until(lambda self : self.browser.find_element_by_tag_name('body'))
        self.assertIn(result, body.text)

        self.url = ROOT + '/auth/logout'
        self.browser.get(self.url)
        time.sleep(1)
        
