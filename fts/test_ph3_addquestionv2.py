# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS, questiddict
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


@ddt
class AddBasicQuestion(FunctionalTest):

    def setUp(self):
        self.url = f'{ROOT}/auth/login'
        self.browser.get(self.url)

    @data((USERS['USER2'], USERS['PASSWORD2'], 'User2Ph3Quest', 'Yes', 'No', 'Standard'),
          (USERS['USER3'], USERS['PASSWORD3'], 'User3Ph3Quest', 'Yes', 'No', 'Standard'),
          (USERS['USER4'], USERS['PASSWORD4'], 'User4Ph3Quest', 'Yes', 'No', 'Standard'),
          (USERS['USER5'], USERS['PASSWORD5'], 'User5Ph3Quest', 'Yes', 'No', 'Standard'))
    @unpack
    def test_question(self, user, passwd, question, answer1, answer2, resolvemethod):
        global questiddict
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "no_table_email"))
        email.send_keys(user)
        password = self.browser.find_element(By.ID, "no_table_password")
        password.send_keys(passwd)
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(1)

        self.url = ROOT + '/new_question/None/quest'
        self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        questiontext = WebDriverWait(self, 10).until(lambda self:
                                                     self.browser.find_element(By.ID, 'question_questiontext'))
        questiontext.send_keys(question)

        # resmethod = WebDriverWait(self, 10).until(lambda self:
        #                                          self.browser.find_element_by_id("question_resolvemethod"))
        # resmethod.send_keys(resolvemethod)

        ans1 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "question_answer1"))
        ans1.send_keys(answer1)
        ans2 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element(By.ID, "question_answer2"))
        ans2.send_keys(answer2)
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(1)

        # Lookof for body in questiongrid
        body = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.TAG_NAME, 'body'))
        self.assertIn(question, body.text)

        alertarea = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, 'alertarea'))
        self.assertIn("ID", alertarea.text)
        recordpos = alertarea.text.find('RecordID')
        if recordpos > 0:
            recordstr = alertarea.text[recordpos + 9:]
            recordval = int(recordstr) if recordstr.isnumeric() else 0
            questiddict[question] = recordval
        self.url = f'{ROOT}/auth/logout'
        self.browser.get(self.url)
        time.sleep(1)
