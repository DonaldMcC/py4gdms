from functional_tests import FunctionalTest, ROOT, USERS, questiddict
import time
from ddt import ddt, data, unpack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# This now uses questidlist and that should allow access to single question
# will need updated as I think answer selection is now not part of DDT but it
# will need to become so in a bit


@ddt
class AnswerQuestion (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)

    @data((USERS['USER2'], USERS['PASSWORD2'], 'In Progress', 'yes', 'User2Ph3Quest'),
          (USERS['USER3'], USERS['PASSWORD3'], 'In Progress', 'no', 'User2Ph3Quest'),
          (USERS['USER4'], USERS['PASSWORD4'], 'Resolved', 'no', 'User2Ph3Quest'),
          (USERS['USER2'], USERS['PASSWORD2'], 'In Progress', 'no', 'User3Ph3Quest'),
          (USERS['USER3'], USERS['PASSWORD3'], 'In Progress', 'no', 'User3Ph3Quest'),
          (USERS['USER4'], USERS['PASSWORD4'], 'Resolved', 'no', 'User3Ph3Quest'))
    @unpack
    def test_answer(self, user, passwd, result, answer, question):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        qid = questiddict.get(question)

        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("signin"))
        email.send_keys(user)
        password = self.browser.find_element_by_id("signpass")
        password.send_keys(passwd)
        submit_button = self.browser.find_element_by_id("login")
        submit_button.click()
        time.sleep(1)

        self.url = ROOT + '/index/questions/' + str(qid)
        self.browser.get(self.url)
        time.sleep(1)

        if answer == 'yes':
            self.browser.find_element(By.CSS_SELECTOR, "td:nth-child(5) > .is-success").click()
        else:
            self.browser.find_element(By.CSS_SELECTOR, "td:nth-child(5) > .is-warning").click()

        time.sleep(1)

        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(result, body.text)

        self.url = ROOT + '/auth/logout'
        self.browser.get(self.url)
        time.sleep(1)
