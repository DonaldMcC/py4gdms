# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first

from functional_tests import FunctionalTest, ROOT, USERS, questidlist, questiddict
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
print(questidlist)


@ddt
class AddBasicAction (FunctionalTest):

    def setUp(self):
        self.url = f'{ROOT}/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "no_table_email"))
        email.send_keys(USERS['USER2'])
        password = self.browser.find_element(By.ID, "no_table_password")
        password.send_keys(USERS['PASSWORD2'])
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(1)

    @data(('/new_question/None/action', 'Reduce world poverty by 20%', 'p2action'),
          ('/new_question/None/issue', 'The world is under-achieving', 'p2issue'))
    @unpack
    def test_question(self, urltxt, itemtext, itemkey):
        self.url = ROOT + urltxt
        self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        # questiontext = self.browser.find_element_by_name('questiontext')
        questiontext = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.NAME, 'questiontext'))
        questiontext.send_keys(itemtext)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        # submit_button = self.browser.find_element_by_css_selector("#submit_record__row input")
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(10)

        # Lookof for body in questiongrid
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
        self.assertIn(itemtext, body.text)

        alertarea = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, 'alertarea'))
        self.assertIn("ID", alertarea.text)
        recordpos = alertarea.text.find('RecordID')
        if recordpos > 0:
            recordstr = alertarea.text[recordpos+9:]
            # print('recstr:'+recordstr)
            recordval = int(recordstr) if recordstr.isnumeric() else 0
            # print(recordval)
            questidlist.append(recordval)
            questiddict[itemkey] = recordval
            # print(questidlist)
