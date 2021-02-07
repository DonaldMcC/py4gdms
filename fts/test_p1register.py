from functional_tests import FunctionalTest, ROOT, USERS
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait
import time


@ddt
class TestRegisterPage (FunctionalTest):
    def setUp(self):      
        self.url = ROOT + '/auth/register'
        get_browser = self.browser.get(self.url)
    @data((USERS['USER2'], USERS['PASSWORD2']), (USERS['USER3'], USERS['PASSWORD3']),
          (USERS['USER4'], USERS['PASSWORD4']), (USERS['USER5'], USERS['PASSWORD5']))

    @unpack
    def test_put_values_in_regester_form(self, user, passwd):
        first_name = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_name("first_name"))
        first_name.clear()
        first_name.send_keys(user)

        username = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_name("username"))
        username.clear()
        username.send_keys(user)

        last_name = self.browser.find_element_by_name("last_name")
        last_name.clear()
        last_name.send_keys(user)

        mailstring = user + '@user.com'
        email = self.browser.find_element_by_name("email")
        email.clear()
        email.send_keys(mailstring)

        password = self.browser.find_element_by_name("password")
        password.clear()
        password.send_keys(passwd)

        verify_password = self.browser.find_element_by_name("password_again")
        verify_password.clear()
        verify_password.send_keys(passwd)

        #data_consent = self.browser.find_element_by_name("data_consent")
        #data_consent.click()

        register_button = self.browser.find_element_by_css_selector("input[type=submit]")
        time.sleep(2)
        register_button.click()

        self.url = ROOT + '/auth/logout'
        get_browser = self.browser.get(self.url)
        time.sleep(1)
