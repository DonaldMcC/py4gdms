# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS, questiddict
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait

@ddt
class AddBasicQuestion (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)

    @data((USERS['USER2'], USERS['PASSWORD2'], 'User2Ph2Quest', 'Yes', 'No', 'Standard'),
          (USERS['USER3'], USERS['PASSWORD3'], 'User3Ph2Quest', 'Yes', 'No', 'Standard'),
          (USERS['USER4'], USERS['PASSWORD4'], 'User 4 Ph2 Quest', 'Yes', 'No', 'Standard'),
          (USERS['USER5'], USERS['PASSWORD5'], 'User 5 Ph2 Quest', 'Yes', 'No', 'Standard'))
    @unpack
    def test_question(self, user, passwd, question, answer1, answer2, resolvemethod):
        global questidlist
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("signin"))
        email.send_keys(user)
        password = self.browser.find_element_by_id("signpass")
        password.send_keys(passwd)
        # submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button = self.browser.find_element_by_id("login")
        submit_button.click()
        time.sleep(1)

        self.url = ROOT + '/new_question/None/quest'
        self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        questiontext = WebDriverWait(self, 10).until(lambda self:
                                     self.browser.find_element_by_id('question_questiontext'))
        questiontext.send_keys(question)

        # resmethod = WebDriverWait(self, 10).until(lambda self:
        #                                          self.browser.find_element_by_id("question_resolvemethod"))
        # resmethod.send_keys(resolvemethod)

        ans1 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("question_answer1"))
        ans1.send_keys(answer1)
        ans2 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("question_answer2"))
        ans2.send_keys(answer2)
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)

        # Lookof for body in questiongrid
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(question, body.text)

        alertarea = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id('alertarea'))
        self.assertIn("ID", alertarea.text)
        recordpos = alertarea.text.find('RecordID')
        if recordpos > 0:
            recordstr = alertarea.text[recordpos + 9:]
            recordval = int(recordstr) if recordstr.isnumeric() else 0
            questiddict[question] = recordval
        self.url = ROOT + '/auth/logout'
        self.browser.get(self.url)
        time.sleep(1)
