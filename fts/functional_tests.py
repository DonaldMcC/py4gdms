#!/usr/bin/env python
# this is now using the HTLMLTestrunner approach - however cant get that working to file other than by piping
# at the command line so approach for now is to get command line at main directory and run:
# python .\fts\functional_tests.py >testddmm.html  to get the file and then open in a browser
#
import unittest
import HTMLTestRunner
import sys
try:
	from urllib2 import urlopen
except ImportError:
	from urllib.request import urlopen
from selenium import webdriver
import subprocess
import sys
import os.path

sys.path.append('./fts/lib')


# ROOT = 'http://localhost:8080/gdms'
ROOT = 'http://localhost:8000/py4test'
# ROOT = 'http://localhost:8081/gdms'
# ROOT = 'https://www.netdecisionmaking.com/gdmssql'

NUMCYCLES = 2  # Reduce this for quicker runs
CACHETIME = 1
STARTSERVER = False

# may update these later but possibly just have 3 options for now
USERS={'USER1':'User1','PASSWORD1':'Testuser1',
        'USER2':'User2','PASSWORD2':'Testuser2','USER3':'User3','PASSWORD3':'Testuser3','USER4':'User4','PASSWORD4':'Testuser4',
       'USER5':'User5','PASSWORD5':'Testuser5','USER6':'User6','PASSWORD6':'Testuser6','USER7':'User7','PASSWORD7':'Testuser7',
       'USER8':'User8','PASSWORD8':'Testuser8','USER9':'User9','PASSWORD9':'Testuser9'}

listusers = ['user2', 'user3', 'user4']
questref =  'functest questref'
votequest = 'tempvotetest'
testconfig = ('standard')
# testconfig = ('verify','local')
questidlist=[]  #will store records of questions successfully stored - may need to add more details later

class FunctionalTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global STARTSERVER
        if STARTSERVER:
            self.web2py = start_web2py_server()
        # self.browser = webdriver.Firefox()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-extensions')

        #self.browser = webdriver.Chrome(r'/home/ubuntu/.virtualenvs/gdms/bin/chromedriver',chrome_options=chrome_options)
        #self.browser = webdriver.Chrome(r'/home/ubuntu/.virtualenvs/gdms/bin/chromedriver',chrome_options=chrome_options)
        self.browser = webdriver.Chrome('d:\python37\chromedriver.exe',chrome_options=chrome_options)
        self.browser.maximize_window()

        #self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(10)

    @classmethod    
    def tearDownClass(self):
        global STARTSERVER
        self.browser.close()
        if STARTSERVER:
            self.web2py.kill()

    def get_response_code(self, url):
        """Returns the response code of the given url

        url     the url to check for 
        return  the response code of the given url
        """

        handler = urlopen(url, timeout=5)
        return handler.getcode()


def start_web2py_server():
    # noreload ensures single process
    #print (os.path.curdir)
    return subprocess.Popen([
            'python', '../../web2py.py', 'runserver', '-a "passwd"', '-p 8001'
    ])

def run_functional_tests(pattern=None):
    print ('running tests')
    if pattern is None:
        tests = unittest.defaultTestLoader.discover('fts')
    else:
        pattern_with_globs = '*%s*' % (pattern,)
        tests = unittest.defaultTestLoader.discover('fts', pattern=pattern_with_globs)

    # neither of these actually write to file so just using >filename.html on the command line
    # runner = unittest.TextTestRunner()
    runner = HTMLTestRunner.HTMLTestRunner(verbosity=2)
    runner.run(tests)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_functional_tests()
    else:
        run_functional_tests(pattern=sys.argv[1])
