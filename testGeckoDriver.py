import time

import logging.handlers
import logging.config
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions


class worknetCrawlerBot():
    def __init__(self):
        self.binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\geckodriver.exe")
        #self.binary = FirefoxBinary("/usr/bin/firefox", log_file=sys.stdout)
        self.hereWork = "worknet_crawling"

        self.currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
            time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

        self.logger = logging.getLogger(self.hereWork + '_logging')

        print('init start', self.binary)


    def setUp(self):
        #self.driver = webdriver.Firefox(firefox_binary = self.binary)

        #self.fp = webdriver.FirefoxProfile()
        #print('setUp', self.fp)

        opts = FirefoxOptions()
        opts.add_argument("--headless")

        self.driver = webdriver.Firefox(firefox_binary=self.binary, firefox_options=opts)

        print('self.driver:', self.driver)


    def worknet_login(self):

        self.setUp()

        driver = self.driver

        userid = 'microscope83'
        userpw = 'Gkstkddbs1!'

        driver.get("http://www.work.go.kr/seekWantedMain.do")

        if driver.find_element_by_id('chkKeyboard').is_selected():
            print('get in')
            driver.execute_script("arguments[0].click();", driver.find_element_by_id('chkKeyboard'))

            driver.find_element_by_id('custId').send_keys(userid)
            driver.find_element_by_id('pwd').send_keys(userpw)

            driver.find_element_by_id('btnLogin').click()

            print(driver.current_url)

            searchURL = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"
            returnResult = self.bringContentBasicData(driver, searchURL)

            driver.get(searchURL)

            print('login success')


        else:
            print('키보드 보안 프로그램으로 인해 해결 불가')

            searchURL = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"
            returnResult = self.bringContentBasicData(driver, searchURL)

            driver.get(searchURL)

            print('login failed')

            driver.close()



if __name__ == "__main__":
    worknetPrj = worknetCrawlerBot()
    worknetPrj.worknet_login()
