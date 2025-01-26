# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class AnswerQuestion (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        email = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "no_table_email"))
        email.send_keys(USERS['USER1'])
        password = self.browser.find_element(By.ID, "no_table_password")
        password.send_keys(USERS['PASSWORD1'])
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(2)

    def test_datasetup(self):
        self.url = f'{ROOT}/datasetup'
        self.browser.get(self.url)
        time.sleep(1)
        # self.browser.execute_script('alert("hi")')
        time.sleep(2)
        body = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
        self.assertIn('Setup has been completed successfully', body.text)
