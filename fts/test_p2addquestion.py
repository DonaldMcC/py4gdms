# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS, CACHETIME, questidlist, questiddict
import time
from selenium.webdriver.support.ui import WebDriverWait


class AddBasicQuestion (FunctionalTest):

    def setUp(self):
        self.url = ROOT + '/auth/login'
        self.browser.get(self.url)
        time.sleep(2)
        email = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("no_table_username"))
        email.send_keys(USERS['USER2'])
        password = self.browser.find_element_by_id("no_table_login_password")
        password.send_keys(USERS['PASSWORD2'])
        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)

    def test_question(self):
        self.url = ROOT + '/new_question/None/quest'
        self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        # questiontext = self.browser.find_element_by_name('questiontext')
        itemtext = "Selenium to be or not to be"
        questiontext = WebDriverWait(self, 10).until(lambda self:
                                                     self.browser.find_element_by_id('question_questiontext'))
        questiontext.send_keys(itemtext)

        ans1 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("question_answer1"))
        ans1.send_keys("be")

        ans2 = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id("question_answer2"))
        ans2.send_keys("not to be")

        submit_button = self.browser.find_element_by_css_selector("input[type=submit]")
        submit_button.click()
        time.sleep(1)
  
        # Lookof for body in questiongrid
        body = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_tag_name('body'))
        self.assertIn(itemtext, body.text)

        alertarea = WebDriverWait(self, 10).until(lambda self: self.browser.find_element_by_id('alertarea'))
        self.assertIn("ID", alertarea.text)
        recordpos = alertarea.text.find('RecordID')
        if recordpos > 0:
            recordstr = alertarea.text[recordpos+9:]
            # print('recstr:'+recordstr)
            recordval=int(recordstr) if recordstr.isnumeric() else 0
            # print(recordval)
            questidlist.append(recordval)
            questiddict['p2quest'] = recordval
        print(questidlist)
        time.sleep(CACHETIME)
