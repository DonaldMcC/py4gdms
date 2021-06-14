from functional_tests import FunctionalTest, ROOT, USERS
import time
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait


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
        # first_name = self.browser.find_element_by_name("first_name")
        first_name = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("firstname"))
        first_name.clear()
        first_name.send_keys(user)

        username = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("username"))
        username.clear()
        username.send_keys(user)
        
        last_name = self.browser.find_element_by_id("lastname")
        last_name.clear()
        last_name.send_keys(user)

        mailstring = user+'@user.com'
        email = self.browser.find_element_by_id("email")
        email.clear()
        email.send_keys(mailstring)

        password = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("password"))
        password.clear()
        password.send_keys(passwd)

        verify_password = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element_by_xpath(r"//div[@id='password2']/input[1]"))
        verify_password.clear()
        verify_password.send_keys(passwd)
        # data_consent = self.browser.find_element_by_name("data_consent")
        # data_consent.click()

        register_button = self.browser.find_element_by_id("submit")

        time.sleep(5)
        register_button.click()
        time.sleep(5)

        # self.url = ROOT + '/auth/login'
        # get_browser = self.browser.get(self.url)

        resultstring = "Registered"
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        time.sleep(5)
        self.assertIn(resultstring, body.text)
