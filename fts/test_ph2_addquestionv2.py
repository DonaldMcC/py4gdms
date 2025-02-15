# These tests are all based on the tutorial at http://killer-web-development.com/
# if registration is successful this may work but lets
# try and get user logged in first


from functional_tests import FunctionalTest, ROOT, USERS, questiddict
from ddt import ddt, data, unpack
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


@ddt
class AddBasicQuestion (FunctionalTest):

    def setUp(self):
        self.url = f'{ROOT}/auth/login'
        self.browser.get(self.url)

    @data((USERS['USER2'], USERS['PASSWORD2'],
           'Which of the following is considered the most effective way to combat climate change',
           'Planting trees in urban areas',
           'Reducing carbon emissions from fossil fuels',
           'Banning plastic straws',
           'Increasing the use of nuclear power',
           'Standard'),
          (USERS['USER3'], USERS['PASSWORD3'],
           'What is a key benefit of artificial intelligence in healthcare?',
           'It replaces human doctors entirely',
           'It allows for faster and more accurate disease diagnosis',
           'It eliminates the need for medical research',
           'It makes hospitals completely automated',
           'Standard'),
          (USERS['USER4'], USERS['PASSWORD4'],
           'Which factor is most critical for global economic development',
           'Increased government control over all industries',
           'Free and fair access to quality education',
           'Dependence on fossil fuel exports',
           'A shift to fully automated jobs',
           'Standard'),
          (USERS['USER5'], USERS['PASSWORD5'],
           'What is one of the most effective strategies to reduce global poverty',
           'Providing direct cash transfers to low-income individuals',
           'Increasing tariffs on international trade',
           'Encouraging rural communities to rely solely on agriculture',
           'Reducing access to financial services',
           'Standard'))
    @unpack
    def test_question(self, user, passwd, question, answer1, answer2, answer3, answer4, resolvemethod):
        global questiddict
        email = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "no_table_email"))
        email.send_keys(user)
        password = self.browser.find_element(By.ID, "no_table_password")
        password.send_keys(passwd)
        submit_button = self.browser.find_element(By.CSS_SELECTOR, "input[type=submit]")
        submit_button.click()
        time.sleep(5)

        self.url = f'{ROOT}/new_question/None/quest'
        self.browser.get(self.url)
        time.sleep(2)  # still getting blank category for some reason but not if loaded manually
        questiontext = WebDriverWait(self, 10).until(lambda self:
                                                     self.browser.find_element(By.ID, 'question_questiontext'))
        questiontext.send_keys(question)

        # resmethod = WebDriverWait(self, 10).until(lambda self:
        #                                          self.browser.find_element_by_id("question_resolvemethod"))
        # resmethod.send_keys(resolvemethod)

        ans1 = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "question_answer1"))
        ans1.send_keys(answer1)
        ans2 = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "question_answer2"))
        ans2.send_keys(answer2)
        time.sleep(3)
        ans3 = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "question_answer3"))
        ans3.send_keys(answer3)
        ans4 = WebDriverWait(self, 10).until(
            lambda self: self.browser.find_element(By.ID, "question_answer4"))
        ans4.send_keys(answer4)
        # adding quite a bit of time here for AI response to get populated
        time.sleep(3)

        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
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
