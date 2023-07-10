from functional_tests import FunctionalTest, ROOT, USERS
import time
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# element = WebDriverWait(driver, 10).until(lambda driver : driver.find_element_by_id("createFolderCreateBtn"))


@ddt
class TestRegisterPage (FunctionalTest):
    def setUp(self):     
        self.url = ROOT + '/auth/register'
        self.browser.get(self.url)

    # def test_can_view_register_page(self):
    #    response_code = self.get_response_code(self.url)        
    #    self.assertEqual(response_code, 200)    

    # def test_has_right_title(self):
    #    title = self.browser.title        
    #    #self.assertEqual(u'Net Decision Making: Registration', title)
    #    self.assertIn('Networked Decision Making', title)

    @data((USERS['USER1'], USERS['PASSWORD1']))
    @unpack
    def test_put_values_in_regester_form(self, user, passwd):

        username = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "auth_user_username"))
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

        mailstring = user+'@user.com'
        email = self.browser.find_element(By.ID, "auth_user_email")
        email.clear()
        email.send_keys(mailstring)

        password = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "auth_user_password"))
        password.clear()
        password.send_keys(passwd)

        password2 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(
            By.ID, "no_table_password_again"))
        password2.clear()
        password2.send_keys(passwd)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        data_consent = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(
            By.ID, "auth_user_data_consent"))

        data_consent.click()

        # self.browser.find_element_by_id("auth_user_status").send_keys("bla")
        # self.browser.find_element_by_id("auth_user_test").send_keys("bla")
        # self.browser.find_element_by_id("auth_user_notify").click()
        # dropdown = self.browser.find_element_by_id("auth_user_notify")
        # dropdown.find_element_by_xpath("//option[. = 'm']").click()
        # self.browser.find_element_by.css_selector("option:nth-child(2)").click()
        # self.browser.find_element_by.css_selector("div:nth-child(1) > input").click()
        # self.browser.find_element_by.css_selector(".close").click()

        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()

        # register_button = self.browser.find_element_by_id("submit")

        # time.sleep(5)
        # register_button.click()
        time.sleep(1)

        resultstring = "registered"
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
        time.sleep(15)
        self.assertIn(resultstring, body.text)
