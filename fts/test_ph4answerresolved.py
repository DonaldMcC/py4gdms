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

    # This should allow user 5 to change answer - but maybe not doing so - to be further investigated
    @data((USERS['USER5'], USERS['PASSWORD5'], 'No', 'Answer recorded'),
          (USERS['USER6'], USERS['PASSWORD6'], 'No', 'In Progress'),
          )
    @unpack
    def test_answer(self, user, passwd, answer, result):
        self.url = f'{ROOT}/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        qid = questiddict.get('ph4quest')

        email = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "no_table_email"))
        email.send_keys(user)
        password = self.browser.find_element(By.ID, "no_table_password")
        password.send_keys(passwd)
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        self.url = f'{ROOT}/viewquest/{qid}'
        self.browser.get(self.url)
        #self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        body = WebDriverWait(self, 10).until(
            lambda self:self.browser.find_element(By.CSS_SELECTOR, ".btn-danger").click())

        body = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
        self.assertIn(result, body.text)

        self.url = f'{ROOT}/auth/logout'
        self.browser.get(self.url)
        time.sleep(1)
