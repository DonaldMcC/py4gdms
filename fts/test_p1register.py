from functional_tests import FunctionalTest, ROOT, USERS
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By


@ddt
class TestRegisterPage (FunctionalTest):
    def setUp(self):      
        self.url = ROOT + '/auth/register'
        self.browser.get(self.url)
    @data((USERS['USER2'], USERS['PASSWORD2']), (USERS['USER3'], USERS['PASSWORD3']),
          (USERS['USER4'], USERS['PASSWORD4']), (USERS['USER5'], USERS['PASSWORD5']),
          (USERS['USER6'], USERS['PASSWORD6']))

    @unpack
    def test_put_values_in_regester_form(self, user, passwd):
        # first_name = self.browser.find_element_by_name("first_name")
        username = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "auth_user_username"))
        username.clear()
        username.send_keys(user)

        # first_name = self.browser.find_element_by_name("first_name")
        first_name = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "auth_user_first_name"))
        first_name.clear()
        first_name.send_keys(user)

        last_name = self.browser.find_element(By.ID, "auth_user_last_name")
        last_name.clear()
        last_name.send_keys(user)

        mailstring = user + '@user.com'
        email = self.browser.find_element(By.ID, "auth_user_email")
        email.clear()
        email.send_keys(mailstring)

        password = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id(By.ID, "auth_user_password"))
        password.clear()
        password.send_keys(passwd)

        password2 = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "no_table_password_again"))
        password2.clear()
        password2.send_keys(passwd)

        # data_consent = self.browser.find_element_by_name("data_consent")
        # data_consent.click()

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(1)

        # self.url = ROOT + '/auth/login'
        # get_browser = self.browser.get(self.url)

        resultstring = "registered"
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
        self.assertIn(resultstring, body.text)
