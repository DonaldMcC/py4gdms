from apps.py4gdms.test_json import return_text
from functional_tests import FunctionalTest, ROOT, USERS, framework
import time
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from playwright.sync_api import sync_playwright



@ddt
class TestRegisterPage (FunctionalTest):
    def setUp(self):
        global framework
        if framework == 'Selenium':
            self.url = f'{ROOT}/auth/register'
            self.browser.get(self.url)
        else:  #playwright
            self.page = self.browser.new_page()
            self.url = f'{ROOT}/auth/login'
            self.page.goto(self.url)

    @data((USERS['USER1'], USERS['PASSWORD1']))
    @unpack
    def test_put_values_in_regester_form(self, user, passwd):
        global framework

        if framework == 'Selenium':
            username = WebDriverWait(self, 10).until(
                lambda self: self.browser.find_element(By.ID, "auth_user_username"))
            username.clear()
            username.send_keys(user)

            # first_name = self.browser.find_element_by_name("first_name")
            first_name = WebDriverWait(self, 10).until(
                lambda self: self.browser.find_element(By.ID, "auth_user_first_name"))
            first_name.clear()
            first_name.send_keys(user)

            last_name = self.browser.find_element(By.ID, "auth_user_last_name")
            last_name.clear()
            last_name.send_keys(user)

            mailstring = f'{user}@user.com'
            email = self.browser.find_element(By.ID, "auth_user_email")
            email.clear()
            email.send_keys(mailstring)

            password = WebDriverWait(self, 10).until(
                lambda self: self.browser.find_element(By.ID, "auth_user_password"))
            password.clear()
            password.send_keys(passwd)

            password2 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(
                By.ID, "no_table_password_again"))
            password2.clear()
            password2.send_keys(passwd)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            data_consent = WebDriverWait(self, 10).until(
                lambda self: self.browser.find_element(By.ID, "auth_user_data_consent"))

            data_consent.click()

            submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
            submit_button.click()

            time.sleep(1)

            resultstring = "registered"
            body = WebDriverWait(self, 10).until(
                lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
            time.sleep(15)
            self.assertIn(resultstring, body.text)
        else: # playwright
            pass

        return

