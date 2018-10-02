#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import logging.handlers
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mysqlConnection
from PycharmProjects.crawling_modules_v1804.crawlerBot_package_JUST_TEST.NotUsingJSONDATAType import mysqlConnection_jeniel


class facebookCrawlerBot:
    def __init__(self):
        print('start')

global driver
global user_id
global user_pass
global pagelet_dict_data
global t_score_count
global returnValue_facebook

global hereWork
hereWork = 'FaceBook'

currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

#log 기본 설정 - 파일로 남기기 위해 [filename='./log/fb_logging_' + currTime] parameter로 추가한다.
#logging.basicConfig(filename='C:/python_project/just_project/PycharmProjects/log/' + hereWork + 'crawlerbot_logging_' + currTime, level=logging.DEBUG)

#logger 인스턴스를 생성 및 로그 레벨 설정
logger = logging.getLogger(hereWork+'_logging')
logger.setLevel(logging.DEBUG)

# formatter 생성
formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

#fileHandler와 StreamHandler를 생성
file_max_bytes = 10*1024*1024   # log file size : 10MB
fileHandler = logging.handlers.RotatingFileHandler('C://python_project/aster879_project/PycharmProjects/log/' + hereWork + 'crawlerbot_logging_' + currTime, maxBytes=file_max_bytes, backupCount=10)
streamHandler = logging.StreamHandler()

# handler에 fommater 세팅
fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

#Handler를 logging에 추가
logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

#logging
logging.debug(hereWork + '_crawlerbot_debugging on' + currTime)
logging.info('info')
logging.warning('warning')
logging.error('error')
logging.critical('critical')


def login_facebook(self, loginCnt, userFacebookPageId, insertedUserName, requestClient):
    start_time_all = time.time()

    returnValue_facebook = False

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    prefs = {}
    prefs['profile.default_content_setting_values.notifications'] = 2
    chrome_options.add_experimental_option('prefs', prefs)
    driver_chrome = r"C:\python_project\aster879_project\PycharmProjects\chromedriver.exe"

    # go to Google and click the I'm Feeling Lucky button
    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)

    # url
    driver.get('https://www.facebook.com')

    user_id = '01027746254'
    user_pass = 'Gkstkddbs4$'

    # id and password
    driver.find_element_by_name('email').send_keys(user_id)
    driver.find_element_by_name('pass').send_keys(user_pass)

    # try login : 로그인 버튼의 id 값이 아래의 범위 내에서 무작위로 변경되기 때문에 이에 대한 대응차원임.
    try:
        driver.find_element_by_xpath('// *[ @ id = "u_0_2"]').click()
        login_or_not = True
    except Exception as ex1:
        print('로그인 버튼 id 값이 u_0_2 가 아닙니다.', ex1)

        try:
            driver.find_element_by_xpath('// *[ @ id = "u_0_3"]').click()
            login_or_not = True
        except Exception as ex2:
            print('로그인 버튼 id 값이 u_0_3 이 아닙니다.', ex2)

            try:
                driver.find_element_by_xpath('// *[ @ id = "u_0_4"]').click()
                login_or_not = True
            except Exception as ex3:
                print('로그인 버튼 id 값이 u_0_4 가 아닙니다.', ex3)

                try:
                    driver.find_element_by_xpath('// *[ @ id = "u_0_d"]').click()
                    login_or_not = True
                except Exception as ex4:
                    print('로그인 버튼 id 값이 u_0_d 가 아닙니다.', ex4)

                    try:
                        driver.find_element_by_xpath('// *[ @ id = "u_0_b"]').click()
                        login_or_not = True
                    except Exception as ex5:
                        print('로그인 버튼 id 값이 u_0_b 가 아닙니다.', ex5)
                        login_or_not = False

                        '''

                        try:
                            driver.find_element_by_xpath('// *[ @ id = "u_0_a"]').click()
                            login_or_not = True
                        except Exception as ex6:
                            print('로그인 버튼 id 값이 u_0_f 가 아닙니다.', ex6)

                            try:
                                driver.find_element_by_xpath('// *[ @ id = "u_0_e"]').click()
                                login_or_not = True
                            except Exception as ex7:
                                print('로그인 버튼 id 값이 u_0_e 가 아닙니다. 로그인 실패입니다. 소스를 다시 분석하세요.', ex7)
                                login_or_not = False
                        '''

    loginCnt += 1
    # calling next Function
    user_facebook_page_id = userFacebookPageId

    # for test user facebook page id
    directlyTypedUserName = insertedUserName

    print('driver.current_url : ', driver.current_url)
    returnedValue_from_method = profileTextDataCrawling(login_or_not, loginCnt, user_facebook_page_id, directlyTypedUserName, driver, requestClient)

    if returnedValue_from_method['trueOrFalse'] == True:
        returnValue_facebook = True

    end_time = time.time() - start_time_all
    print('데이터 기반 크롤링 총 구동 시간 :', end_time)

    driver.close()

    #처음 호출한 웹서버에 리턴
    return returnedValue_from_method



def profileTextDataCrawling(loginValue, lgnCnt, insertedUser_fbpage_id, insertedUserName, driver, requestClient):
    returnedValue_profileTextDataCrawling = False
    profileDic = {}
    detailInfo = []


    if (loginValue == False):

        if (lgnCnt > 3):
            print('페이스북 로그인에 최종 실패하여, 사용자 정보 크롤링이 불가합니다.')
            driver.close()
        else:
            print('프로그램을 중지하시고, 페이스북 로그인 정보를 다시 확인하시기 바랍니다.')
            login_facebook(lgnCnt)

    elif (loginValue == True):
        print('login success!')

    user_fbpage_id = insertedUser_fbpage_id
    User_timeLine_site_url_addr = 'https://www.facebook.com/' + user_fbpage_id

    #returnedResultList = getDetailInfoListType(user_fbpage_id, driver, lgnCnt, insertedUserName)
    #print('미리 취득한 사용자 세부 데이터 -> ', returnedResultList)

    # No.1 -> 세부정보 선 취득_Dictionary type :
    returnedResultDict = getDetailInfoDictionaryType(user_fbpage_id, driver, lgnCnt, insertedUserName, requestClient)
    print('사용자 페이스북 상의 세부 데이터 -> ', returnedResultDict)

    # wait for loading & set(alter) driver's url
    driver.get(User_timeLine_site_url_addr)

    # get page source in raw state
    html_src_chrome = driver.page_source

    # beautifulsoup4 initialization :  get the page source in soup type(like text).
    fb_tmln_soup = bs(html_src_chrome, 'html.parser')

    # get applicant's name
    usernamefromDirect = insertedUserName

    profileDic['페이스북페이지ID'] = user_fbpage_id
    detailInfo.append('페이스북페이지ID:'+user_fbpage_id)

    try:
        user_name = fb_tmln_soup.select('#fb-timeline-cover-name > a')[0].text
        print('페이스북 상의 사용자 이름 : ', user_name)
        profileDic['사용자이름'] = user_name

        detailInfo.append('@사용자이름:' + user_name)

    except:
        print('페이스북 사용자 이름을 가져올 수 없습니다.')
        user_name = usernamefromDirect
        profileDic['사용자이름'] = user_name

        detailInfo.append('@사용자이름:' + user_name)

    if user_name == usernamefromDirect:
        print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치합니다.')

        detailInfo.append('@페이스북 사용자 이름과 이력서의 신청인 이름이 일치합니다.')

    else:
        print('페이스북 사용자 이름과 이력서의 신청인 이름이 일치하지 않습니다.')

        detailInfo.append('@페이스북 사용자 이름과 이력서의 신청인 이름이 일치하지 않습니다.')

    # DATA crawling and parsing part
    # Got scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 소개 글
    try:
        # 해당 글 영역 존재 여부
        intro_text_title = fb_tmln_soup.select(
            'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > span')
        if not intro_text_title:
            print('소개글 영역이 존재하지 않습니다.')
            exist_text_or_not = False
        else:
            print(intro_text_title[0].text)  # '소개'

            try:
                # 소개글
                intro_text_detail = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div#profile_intro_card_bio > div > div > div > span')
                print('소개글 : ', intro_text_detail[0].text)
                #returnedResultList.append(intro_text_detail[0].text.replace(' ', ''))
                profileDic['소개글'] = intro_text_detail[0].text.replace(' ', '')

                detailInfo.append('@'.join(profileDic['소개글']))


            except Exception as ew:
                print("소개글 게시판 HTML 구조가 변경되어 다시 검색합니다. --> ", ew)

                intro_text_detail2 = fb_tmln_soup.select(
                    'li.fbTimelineTwoColumn.fbTimelineUnit.clearfix > div > div#intro_container_id > div:nth-of-type(1) > div > div')
                intro_text_detail = intro_text_detail2
                print('소개글 : ', intro_text_detail[0].text)
                #returnedResultList.append(intro_text_detail[0].text.replace(' ', ''))
                profileDic['소개글'] = intro_text_detail[0].text.replace(' ', '')

                detailInfo.append('@'.join(profileDic['소개글']))


            print('1차 dictionary 결과물 출력 -> ', profileDic)
    except Exception as e:
        print('[소개글]게시된 소개글의 값들이 존재하지 않습니다.-> ', e)

    try:
        profile_list_test_old = fb_tmln_soup.select(
            'div#intro_container_id > div:nth-of-type(2) > div:nth-of-type(1) > ul > li')
        profile_list_detail_text_01_old = fb_tmln_soup.select(
            'div#intro_container_id > div:nth-of-type(2) > div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')

        lengthOfProfileList = len(profile_list_test_old)
        lengthOfDetailListText = len(profile_list_detail_text_01_old)

        originalHTMLDOMRegion = 'div#intro_container_id > div:nth-of-type(2) >'
        alteredHTMLDOMRegion = 'div#intro_container_id > div:nth-of-type(1) >'

        # DOM 구조 변경에 따른 경로 수정
        if lengthOfProfileList == 0:

            # 경로가 변경되었을 경우, 경로 변경
            profile_list_test = fb_tmln_soup.select(alteredHTMLDOMRegion + ' div:nth-of-type(1) > ul > li')
            print('(altered)프로필 영역 개수 ->', len(profile_list_test))
            profileDic['프로필게시개수'] = str(len(profile_list_test))
            originalHTMLDOMRegion = alteredHTMLDOMRegion
        else:

            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_list_test = fb_tmln_soup.select(originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li')
            print('(original)프로필 영역 개수 ->', len(profile_list_test))
            profileDic['프로필게시개수'] = str(len(profile_list_test))

        if lengthOfDetailListText == 0:

            # 경로가 변경되었을 경우, 경로 변경
            profile_list_detail_text_01 = fb_tmln_soup.select(
                alteredHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
            print('(altered) 값 ->', len(profile_list_detail_text_01))
            originalHTMLDOMRegion = alteredHTMLDOMRegion
        else:

            # 경로가 변경되지 않았을 경우, 기존의 경로대로
            profile_list_detail_text_01 = fb_tmln_soup.select(
                originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(1) > div > div > div > div')
            print('(original)값 ->', len(profile_list_detail_text_01))

        if not profile_list_detail_text_01:

            print('사용자가 프로필 정보를 등록하지 않았습니다.')
        else:
            print('프로필 정보_01 :', profile_list_detail_text_01[0].text)
            #returnedResultList.append(profile_list_detail_text_01[0].text.replace(' ', ''))
            #returnedResultDict['프로필 정보 No.01'] = profile_list_detail_text_01[0].text.replace(' ', '')


        profileDataList = []
        prf = 0
        try:
            while prf < len(profile_list_test):
                key = '프로필정보_0' + str(int(prf + 1))
                print('key : ', key)

                value = fb_tmln_soup.select(
                    originalHTMLDOMRegion + ' div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                        int(prf + 1)) + ') > div > div > div > div')[0].text.replace(" ", "")
                print('value : ', value)

                profileDic[key] = value
                profileDataList.append(value)

                prf += 1

            detailInfo = detailInfo + profileDataList
            profileDic['전체프로필정보'] = '__'.join(profileDataList)


        except:
            print('더이상 가져올 수 있는 정보가 없습니다.')
        print('프로필 정보 [Dictionary type] :', profileDic)
        #print('프로필 정보 사이즈 [Dictionary type] :', len(profileDic))

        returnedResultDict = dict(returnedResultDict, **profileDic)
    except Exception as e:
        print('프로필 정보 취득 중 오류-> ', e)

    #print('결과 [List type]: ', returnedResultList)
    print('@@@@@_결과 [Dictionary type]: ', returnedResultDict)


    tcm_score = {}

    # 대상자의 현재 거주지 또는 출신학교 소재지
    t_score_count = 0
    c_score_count = 0

    t_score_count_detail = 0
    c_score_count_detail = 0


    DictionaryValue_list = returnedResultDict.values()


    for search_t in DictionaryValue_list:
        try:
            if '남성' in search_t:
                t_score_count_detail = 0
                print('성별 정보 검색 중...')

                print('가산 근거 : 남성일 경우 근속 기간이 여성보다 길기 때문에 70점이 가산 됩니다.')
                t_score_count_detail += 50
                t_score_count += t_score_count_detail

                detailInfo.append('__가산근거:남성일경우근속기간이_여성보다_길기때문에_70점이_가산됩니다.__')

            elif '여성' in search_t:
                t_score_count_detail = 0
                print('성별 정보 검색 중...')

                print('가산 근거 : 여성일 경우 근속 기간이 남성보다 짧기 때문에 50점이 가산 됩니다.')

                detailInfo.append('__가산근거:남성일경우근속기간이_여성보다_길기때문에_50점이_가산됩니다.__')

                t_score_count_detail += 25
                t_score_count += t_score_count_detail

            # try No.1 : 지역관련 정보 검색
            if '근무' in search_t:
                print('근무지 정보 검색 중...')
                t_score_count_detail = 0
                # print("%%", t_score_count)

                if '서울' in search_t:
                    print('가산 근거 : 근무지가 서울일 경우 60점이 가산 됩니다.')

                    detailInfo.append('__가산근거:근무지가_서울일경우_60점이_가산됩니다.__')

                    t_score_count_detail += 60
                    t_score_count += t_score_count_detail
                    # print("%%", t_score_count)
                elif '경기' in search_t:
                    print('가산 근거 : 근무지가 경기일 경우 40점이 가산됩니다.')

                    detailInfo.append('__가산근거:근무지가_서울일경우_40점이_가산됩니다.__')
                    t_score_count_detail += 40
                    t_score_count += t_score_count_detail
                    # print("%%", t_score_count)
                else:
                    print('가산 근거 : 근무지가 비-수도권일 경우 20점이 가산됩니다.')

                    detailInfo.append('__가산근거:근무지가_서울일경우_20점이_가산됩니다.__')

                    t_score_count_detail += 20
                    t_score_count += t_score_count_detail
                    # print("%%", t_score_count)

            # 학력사항 정보 검색
            if '공부했음' in search_t:
                if '졸업' in search_t:
                    if '대학원' in search_t:
                        print('대학원 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            print('가산 근거 : 출신 대학원 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학원소재지가_서울일경우_60점이_가산됩니다.__')
                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학원 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학원소재지가_서울일경우_40점이_가산됩니다.__')
                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

                    elif '대학교' in search_t:
                        print('대학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            print('가산 근거 : 출신 대학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학교 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

                    elif '고등학교' in search_t:
                        print('고등학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 고등학교 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                    else:
                        print('대학(2~3년제 대학) 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                else:
                    if '대학교' in search_t:
                        print('대학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울대' or '중앙대' or '덕성여' or '서울교육대' or '홍익대' or '이화여' or '서울시립대' or '동국대' or '서울여' or '연세대' or '명지대' or '숙명여' or '고려대' or '상명대' or '동덕여' or '서강대' or '삼육대' or '국민대' or '서울과학기술대' or '한국체육대' or '성신여' or '한국외' or '숭실대' or '총신대' or '세종대' or '한국종합예술' or '한성대' or '서경대' or '성공회대' in search_t:
                            print('가산 근거 : 출신 대학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학교 소재지가 경기일 경우 30점이 가산됩니다.')

                            detailInfo.append('__출신대학교소재지가_서울일경우_30점이_가산됩니다.__')

                            t_score_count_detail += 30
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

                    elif '고등학교' in search_t:
                        print('고등학교 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 고등학교 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_40점이_가산됩니다.__')
                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 고등학교 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신고등학교소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                    else:
                        print('대학(2~3년제 대학) 소재지 정보 검색 중...')
                        t_score_count_detail = 0
                        # print("%%", t_score_count)

                        if '서울' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 서울일 경우 60점이 가산 됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_60점이_가산됩니다.__')

                            t_score_count_detail += 60
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        elif '경기' in search_t:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 경기일 경우 40점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_40점이_가산됩니다.__')

                            t_score_count_detail += 40
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)
                        else:
                            print('가산 근거 : 출신 대학(2~3년제 대학) 소재지가 비-수도권일 경우 20점이 가산됩니다.')

                            detailInfo.append('__출신대학(2~3년제대학)소재지가_서울일경우_20점이_가산됩니다.__')

                            t_score_count_detail += 20
                            t_score_count += t_score_count_detail
                            # print("%%", t_score_count)

        except Exception as e_addr:
            print('T SCORE EXCEPTION : ', e_addr)

    print('T SCORE :', t_score_count)
    print()



    print('C_SCORE를 산출하겠습니다.')
    # C_SCORE
    # 거주지, 출신지, 팔로우 수 (returnedResult : 미리 받아온 세부 데이터)이용하여 C_SCORE 산출하기


    like_cnt_int = 0
    cnt_like_img = 0
    for search_c in DictionaryValue_list:
        try:
            if '거주' in search_c:
                print('거주지 정보 검색 중...')
                c_score_count_detail = 0
                # print("%%", c_score_count)

                if '서울' in search_c:
                    print('가산 근거 : 거주지가 서울일 경우 70점이 가산 됩니다.')

                    detailInfo.append('__거주지가_서울일경우_70점이_가산됩니다.__')

                    c_score_count_detail += 70
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif '경기' in search_c:
                    print('가산 근거 : 거주지가 경기일 경우 40점이 가산됩니다.')

                    detailInfo.append('__거주지가_서울일경우_40점이_가산됩니다.__')

                    c_score_count_detail += 40
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                else:
                    print('가산 근거 : 거주지가 비-수도권일 경우 30점이 가산됩니다.')

                    detailInfo.append('__거주지가_서울일경우_30점이_가산됩니다.__')

                    c_score_count_detail += 30
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)

            if '출신' in search_c:
                print('출신지 정보 검색 중...')
                c_score_count_detail = 0
                # print("%%", c_score_count)

                if '서울' in search_c:
                    print('가산 근거 : 출신지가 서울일 경우 70점이 가산 됩니다.')

                    detailInfo.append('__출신지가_서울일경우_70점이_가산됩니다.__')

                    c_score_count_detail += 70
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                elif '경기' in search_c:
                    print('가산 근거 : 출신지가 경기일 경우 40점이 가산됩니다.')

                    detailInfo.append('__출신지가_서울일경우_40점이_가산됩니다.__')

                    c_score_count_detail += 40
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)
                else:
                    print('가산 근거 : 출신지가 비-수도권일 경우 30점이 가산됩니다.')

                    detailInfo.append('__출신지가_서울일경우_30점이_가산됩니다.__')

                    c_score_count_detail += 30
                    c_score_count += c_score_count_detail
                    # print("%%", c_score_count)

            if '팔로우' in search_c:

                followCntVal = str(search_c).split('명이')
                followCnt = int(followCntVal[0])
                print('팔로우 수: ', followCnt)
                c_score_count_detail = 0

                if followCnt >= 50:
                    print('팔로워 수가 50명 이상일 경우 50점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_50점이_가산됩니다.__')

                    c_score_count_detail += 50
                    c_score_count += c_score_count_detail

                elif 40 <= followCnt < 50:
                    print('팔로워 수가 40명 이상 50명 미만일 경우 40점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_40점이_가산됩니다.__')

                    c_score_count_detail += 40
                    c_score_count += c_score_count_detail

                elif 30 <= followCnt < 40:
                    print('팔로워 수가 30명 이상 40명 미만일 경우 30점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_30점이_가산됩니다.__')

                    c_score_count_detail += 30
                    c_score_count += c_score_count_detail

                elif 20 <= followCnt < 30:
                    print('팔로워 수가 20명 이상 30명 미만일 경우 20점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_20점이_가산됩니다.__')

                    c_score_count_detail += 20
                    c_score_count += c_score_count_detail

                elif 10 <= followCnt < 20:
                    print('팔로워 수가 10명 이상 20명 미만일 경우 10점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_10점이_가산됩니다.__')

                    c_score_count_detail += 10
                    c_score_count += c_score_count_detail

                elif 1 <= followCnt < 10:
                    print('팔로워 수가 1명 이상 10명 미만일 경우 5점이 가산됩니다.')

                    detailInfo.append('__팔로워수가_50명이상일경우_5점이_가산됩니다.__')

                    c_score_count_detail += 5
                    c_score_count += c_score_count_detail

                else:
                    print('팔로워가 없으므로 가산점이 부여되지 않습니다. ')
                    detailInfo.append('팔로워가_없으므로_가산점이_부여되지_않습니다.')

        except Exception as e_c:
            print('C SCORE EXCEPTION :', e_c)

    # (returnedResult : 미리 받아온 세부 데이터)를 이용하지 않고, 친구 수 값을 추출하여 C_SCORE를 산출하기
    # friend count
    try:
        autoScrolled_data_soup_html_result = autoScroller(driver)
        userContent_FriendList = autoScrolled_data_soup_html_result.find('div', attrs={
            'id': 'profile_timeline_tiles_unit_pagelets_friends'})


        if userContent_FriendList:
            print('친구 리스트 공개 중입니다.')
            # friendsCnt_str = autoScrolled_data_soup_html_result.select('profile_timeline_tiles_unit_pagelets_friends > li > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(2) > div > span')[0].text
            friendsCnt_str = autoScrolled_data_soup_html_result.select(
                '#profile_timeline_tiles_unit_pagelets_friends > li > div > div:nth-of-type(1) > div > div.clearfix._3-8t._2pi4 > div > div > div:nth-of-type(2) > div > span._50f8._2iem > a')[
                0].text

            print(friendsCnt_str)
            friendsCnt = int(friendsCnt_str.split('명')[0].replace(',', ''))

            returnedResultDict['친구수'] = int(friendsCnt_str.split('명')[0].replace(',', ''))

            print('친구 수 : ', friendsCnt)
            if friendsCnt >= 500:
                print('친구 수가 500명 이상일 경우 70점이 가산됩니다.')

                detailInfo.append('친구수가_500명이상일경우_70점이_가산됩니다.')

                c_score_count_detail += 70
                c_score_count += c_score_count_detail

            elif 400 <= friendsCnt < 500:
                print('친구 수가 400명 이상 500명 미만일 경우 60점이 가산됩니다.')

                detailInfo.append('친구 수가 400명 이상 500명 미만일 경우_60점이_가산됩니다.')

                c_score_count_detail += 60
                c_score_count += c_score_count_detail

            elif 300 <= friendsCnt < 400:
                print('친구 수가 300명 이상 400명 미만일 경우 50점이 가산됩니다.')

                detailInfo.append('친구 수가 300명 이상 400명 미만일 경우 50점이 가산됩니다.')

                c_score_count_detail += 50
                c_score_count += c_score_count_detail

            elif 200 <= friendsCnt < 300:
                print('친구 수가 200명 이상 300명 미만일 경우 30점이 가산됩니다.')

                detailInfo.append('친구 수가 200명 이상 300명 미만일 경우 30점이 가산됩니다.')

                c_score_count_detail += 30
                c_score_count += c_score_count_detail

            elif 100 <= friendsCnt < 200:
                print('친구 수가 100명 이상 200명 미만일 경우 20점이 가산됩니다.')

                detailInfo.append('친구 수가 100명 이상 200명 미만일 경우 20점이 가산됩니다.')

                c_score_count_detail += 20
                c_score_count += c_score_count_detail

            elif 1 <= friendsCnt < 100:
                print('친구 수가 1명 이상 100명 미만일 경우 10점이 가산됩니다.')

                detailInfo.append('친구 수가 1명 이상 100명 미만일 경우 10점이 가산됩니다.')

                c_score_count_detail += 10
                c_score_count += c_score_count_detail

            else:
                print('친구가 없으므로 가산점이 부여되지 않습니다. ')
                detailInfo.append('친구가 없으므로 가산점이 부여되지 않습니다.')
        else:
            print('친구 리스트가 비공개로 설정되어 있습니다.')
            detailInfo.append('친구 리스트가 비공개로 설정되어 있습니다.')

    except Exception as ex:
        print('친구 수 추적에 실패했습니다.', ex)


    likePushPersonCnt = 0

    try:
        attrValue_like_imgVal = autoScrolled_data_soup_html_result.select(
            'ol[data-pnref="story"] > div._5pcb._4b0l > div._4-u2.mbm._4mrt._5jmm._5pat._5v3q._4-u8 > div._3ccb > div._5pcr.userContentWrapper > div:nth-of-type(2) > form.commentable_item > div.uiUfi.UFIContainer._3-a6._4eno._1blz._5pc9._5vsj._5v9k > div.UFIList > div.UFIRow.UFILikeSentence._4204._4_dr > div.clearfix > div > div._1vaq > div._ipp > div._3t53._4ar-._ipn > span._3t54 > a._3emk._401_')
        cnt_like_img = len(attrValue_like_imgVal)

        attrValue_like_txtVal = autoScrolled_data_soup_html_result.select(
            'ol[data-pnref="story"] > div._5pcb._4b0l > div._4-u2.mbm._4mrt._5jmm._5pat._5v3q._4-u8 > div._3ccb > div._5pcr.userContentWrapper > div:nth-of-type(2) > form.commentable_item > div.uiUfi.UFIContainer._3-a6._4eno._1blz._5pc9._5vsj._5v9k > div.UFIList > div.UFIRow.UFILikeSentence._4204._4_dr > div.clearfix > div > div._1vaq > div._ipp > div._3t53._4ar-._ipn > a._2x4v > span._4arz > span')

        likeManCnt = 0
        likeManCnt1 = 0

        for likePerson in range(len(attrValue_like_txtVal)):
            like_cnt_str = attrValue_like_txtVal[likePerson].text.split('명')[0]

            try:
                like_cnt_int = like_cnt_int + int(like_cnt_str)
                # print('"좋아요" 표시 전체 갯수 :', like_cnt_int)
                likePushPersonCnt += 1

            except ValueError as e_p:
                like_man = attrValue_like_txtVal[likePerson].text
                likePushPersonCnt += 1
                # 갯수가 표시되지 않고 사람 이름이 표시된 경우에 해당함.
                # print('"좋아요"를 누른 사람의 이름:', like_man)
                if '외' in like_man:
                    likeManCntStr = like_man.split('외')[1].strip()
                    likeManCnt1 = int(likeManCntStr.split('명')[0])
                else:
                    print('"좋아요"를 누른 사람의 이름:', like_man)
            likeManCnt += likeManCnt1
        print('Total like man count : ', likeManCnt)

        if likeManCnt >= 5000:
            print('좋아요 표시가 5000개 이상일 경우 70점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 5000개 이상일 경우 70점이 가산됩니다.')

            c_score_count_detail += 70
            c_score_count += c_score_count_detail

        elif 4000 <= likeManCnt < 5000:
            print('좋아요 표시가 4000개 이상 5000개 미만일 경우 60점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 4000개 이상 5000개 미만일 경우 60점이 가산됩니다.')

            c_score_count_detail += 60
            c_score_count += c_score_count_detail

        elif 3000 <= likeManCnt < 4000:
            print('좋아요 표시가 3000개 이상 4000개 미만일 경우 50점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 3000개 이상 4000개 미만일 경우 50점이 가산됩니다.')

            c_score_count_detail += 50
            c_score_count += c_score_count_detail

        elif 2000 <= likeManCnt < 3000:
            print('좋아요 표시가 2000개 이상 3000개 미만일 경우 40점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 3000개 이상 4000개 미만일 경우 50점이 가산됩니다.')

            c_score_count_detail += 40
            c_score_count += c_score_count_detail

        elif 1000 <= likeManCnt < 2000:
            print('좋아요 표시가 1000개 이상 2000개 미만일 경우 30점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 1000개 이상 2000개 미만일 경우 30점이 가산됩니다.')

            c_score_count_detail += 30
            c_score_count += c_score_count_detail

        elif 1 <= likeManCnt < 1000:
            print('좋아요 표시가 1개 이상 1000개 미만일 경우 15점이 가산됩니다.')

            detailInfo.append('좋아요 표시가 1개 이상 1000개 미만일 경우 15점이 가산됩니다.')

            c_score_count_detail += 15
            c_score_count += c_score_count_detail

        else:
            print('좋아요 표시가 없으므로 가산점이 부여되지 않습니다. ')

            detailInfo.append('좋아요 표시가 없으므로 가산점이 부여되지 않습니다. ')


        print('M SCORE :', c_score_count)
    except Exception as e_lk:
        print('좋아요 정보 추출 Exception', e_lk)

    print('좋아요_사람 전체 명수 : ', likePushPersonCnt)
    print('좋아요(image)__표시 전체 갯수: ', cnt_like_img)

    print('C SCORE :', c_score_count)
    print()



    returnedResultDict.update({'좋아요__사람전체명수': likePushPersonCnt, '좋아요(image)__표시전체갯수': cnt_like_img})

    returnedResultDict.update({'DETAIL':detailInfo})

    # T SCORE, C CORE 값을 넘겨 SCM SCORE 산출
    returnedValue_from_method_TCMCountGen = TCMCountGen(t_score_count, c_score_count, returnedResultDict, User_timeLine_site_url_addr, driver, requestClient)

    print('TCMCountGen 의 결과 :', TCMCountGen)

    if returnedValue_from_method_TCMCountGen['trueOrFalse'] == True:
        print('TCM SCORE가 정상 산출 되었습니다.')

    elif returnedValue_from_method_TCMCountGen['trueOrFalse'] == False:
        print('TCM SCORE가 산출 되지 않았습니다.')

    return returnedValue_from_method_TCMCountGen



#getDetailInfo 관련 함수 ========================================================================================
#dictionary type 으로 취합할 정보 : 연락처 정보, 웹사이트 및 소셜 링크 정보, 기본 정보
def getDetailInfoDictionaryType(userPageId, driver, loginCnt, userName, reqClientNm):
    detail_url = 'https://www.facebook.com/'+ userPageId +'/about?section=contact-info&pnref=about'

    driver.get(detail_url)
    html_detail_fb_chrome = driver.page_source
    detail_fb_info_soup = bs(html_detail_fb_chrome, 'html.parser')

    #print('T_SCORE를 산출하겠습니다.')
    #pagelet_basic_list_data = []

    #[연락처 정보]란 제목
    user_pglet_contactData_title_01 = detail_fb_info_soup.select(
        '#pagelet_contact > div > div:nth-of-type(1) > div > span')

    #[웹사이트 및 소셜 링크]란 제목
    user_pglet_contactData_title_01_2 = detail_fb_info_soup.select(
        '#pagelet_contact > div > div:nth-of-type(2) > div > div > span')

    #[기본 정보]란 제목
    user_pglet_basicData_title_01 = detail_fb_info_soup.select(
        '#pagelet_basic > div > div > span')

    user_pglet_data = detail_fb_info_soup.select('div#pagelet_contact > div > div')
    #print('user_pglet_data = ', user_pglet_data)

    length_user_pglet_data = len(user_pglet_data)

    if length_user_pglet_data == 0:
        print('연락처 정보 & 웹사이트 정보 등 표시 영역 길이 : ', length_user_pglet_data)
        print('페이스북 접속이 원할하지 않아 다시 시도해야 합니다.')
        if loginCnt <= 2:

            userInfoDetailDic = False

            return userInfoDetailDic

            #login_facebook(loginCnt, userPageId, userName)

        else:
            print('페이스북 크롤링을 재 구동하여야 합니다. 작동을 중지합니다.')
            driver.close()

    else:
        print('연락처 정보 & 웹사이트 정보 등 표시 영역 길이 : ', length_user_pglet_data)

        #[연락처 정보] & [소셜링크 및 웹사이트 정보] Dictionary
        contDic = {}
        contDataList = []
        contDataList_webSns = []

        #[기본 정보] Dictionary
        basicDic = {}
        basicDataList = []

        #[연락처 정보]란 취득
        if not user_pglet_contactData_title_01:
            print('사용자가 연락처 정보를 등록하지 않았습니다.')
        else:
            #pagelet_contact
            if '연락처' in user_pglet_contactData_title_01[0].text:
                print(user_pglet_contactData_title_01[0].text)  # 연락처 정보

                # [연락처 정보]란 하단 세부 정보 타이틀
                pagelet_contact_dir_list = 'div#pagelet_contact > div > div:nth-of-type(1) > ul > li'

                # [연락처 정보]란 하단 세부 정보 타이틀 갯수
                length_of_contList = len(detail_fb_info_soup.select(pagelet_contact_dir_list))

                # [연락처 정보]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                conCycle = 0

                try:
                    #하단 세부 정보 길이 만큼 반복문 실행해 key:value 생성
                    while  conCycle < length_of_contList:
                        userContactInfoListTitle = detail_fb_info_soup.select(
                            pagelet_contact_dir_list + ':nth-of-type(' + str(int(conCycle+1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [연락처 정보]란_title
                        key = userContactInfoListTitle.replace(" ", "")
                        #print('연락처 정보_title: ', key)

                        # [연락처 정보]란_value
                        value = detail_fb_info_soup.select(
                            pagelet_contact_dir_list +':nth-of-type(' + str(
                                int(conCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[0].text.replace(" ", "")
                        #print('연락처 정보_value: ', value)

                        contDic[key] = value
                        contDataList.append(value)
                        conCycle += 1

                    #contDic['전체연락처정보'] = '__'.join(contDataList)
                    #print("contDic['전체연락처정보'] :", contDic['전체연락처정보'])

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    #contDic['전체연락처정보'] = '전체연락처정보가없습니다'

                print('연락처 정보 수집 결과[Dictionary type]: ' , contDic)
                #contDic['전체연락처정보'] = '전체연락처정보가없습니다'

        # [웹사이트 및 소셜 링크]란
        if not user_pglet_contactData_title_01_2:
            print('사용자가 웹사이트 및 소셜 링크 정보를 등록하지 않았습니다.')
        else:
            #pagelet_contact
            if '웹사이트' in user_pglet_contactData_title_01_2[0].text:
                print(user_pglet_contactData_title_01_2[0].text)  #웹사이트 및 소셜 링크 정보

                # [웹사이트 및 소셜 링크]란 하단 세부 정보 타이틀
                pagelet_contact_webSite_dir_list = 'div#pagelet_contact > div > div:nth-of-type(2) > div > ul > li'

                # [웹사이트 및 소셜 링크]란 하단 세부 정보 타이틀 갯수
                length_of_contWebSiteList = len(detail_fb_info_soup.select(pagelet_contact_webSite_dir_list))

                # [웹사이트 및 소셜 링크]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                conWebCycle = 0

                try:
                    while  conWebCycle < length_of_contWebSiteList:
                        userContactWebInfoListTitle = detail_fb_info_soup.select(
                            pagelet_contact_webSite_dir_list + ':nth-of-type(' + str(int(conWebCycle+1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [웹사이트 및 소셜 링크]란 title
                        key = userContactWebInfoListTitle.replace(" ", "")
                        print('웹사이트 및 소셜 링크 정보_title: ', key)

                        # [웹사이트 및 소셜 링크]란 value
                        value = detail_fb_info_soup.select(
                            pagelet_contact_webSite_dir_list +':nth-of-type(' + str(
                                int(conWebCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[0].text.replace(" ", "")

                        contDic[key] = value

                        contDataList_webSns.append(value)
                        conWebCycle += 1

                    contDic['웹사이트및소셜링크정보'] = '__'.join(contDataList_webSns)

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    contDic['웹사이트및소셜링크정보'] = ''

                print('웹사이트 및 소셜 링크 정보 수집 결과[Dictionary type]: ' , contDic)

        # [기본 정보]란 취득
        if not user_pglet_basicData_title_01:
            print('사용자가 기본 정보를 등록하지 않았습니다.')
        else:
            #pagelet_basic
            if '기본' in user_pglet_basicData_title_01[0].text:
                print(user_pglet_basicData_title_01[0].text)  # 기본 정보

                # [기본 정보]란 하단 세부 정보 타이틀
                pagelet_basic_dir_list = 'div#pagelet_basic > div > ul > li'

                # [기본 정보]란 하단 세부 정보 타이틀 갯수
                length_of_basicList = len(detail_fb_info_soup.select(pagelet_basic_dir_list))

                # [기본 정보]란 하단 세부 정보에 대한 딕셔너리[key : value => 제목 : 값] 생성
                baseCycle = 0

                try:
                    while  baseCycle < length_of_basicList:
                        userBasicInfoListTitle = detail_fb_info_soup.select(
                            pagelet_basic_dir_list + ':nth-of-type(' + str(
                                int(baseCycle+1)) + ') > div > div:nth-of-type(1)')[0].text

                        # [기본 정보]란 title
                        key = userBasicInfoListTitle.replace(" ", "")

                        # [기본 정보]란 value
                        value = detail_fb_info_soup.select(
                            pagelet_basic_dir_list + ':nth-of-type(' + str(
                                int(baseCycle + 1)) + ') > div > div:nth-of-type(2) > div > div > span')[0].text.replace(" ", "")

                        basicDic[key] = value
                        basicDataList.append(value)

                        baseCycle += 1
                    basicDic['전체기본정보'] = '__'.join(basicDataList)

                except:
                    print('더이상 가져올 수 있는 정보가 존재하지 않습니다.')
                    basicDic['전체기본정보'] = ''

                print('기본 정보 수집 결과 [Dictionary type]: ' , basicDic)

        userInfoDetailDic = dict(basicDic, **contDic)

        print('결과 -> 사용자 페이스북 상의 상세 정보 [Dictionary type] : ', userInfoDetailDic)

        return userInfoDetailDic




#TCM SCORE 산출
def TCMCountGen(tScoreCount, cScoreCount, ResultDict, user_fbpage_url, driver, requestClient):

    print('TCMCountGen에서의 중간결과 :', ResultDict['DETAIL'])


    detailInfoList = '@'.join(ResultDict['DETAIL'])

    print('detailInfoList :', detailInfoList.replace(".", ""))

    returnedValue_TCMCountGen = False

    #dictResult ={}
    print('M_SCORE를 산출하겠습니다.')
    userContent_list_result = autoScrollerUserWrapperContents(driver)

    if userContent_list_result is not None:
        totalPicCnt = autoScroller_MSCORE(user_fbpage_url, driver)

        prfl_vodCnt = 0
        prfl_picCnt = 0
        contentCnt = 0

        m_score_count = 0
        m_score_count_detail = 0

        # 동영상, 사진 갯수 추출
        for contntLength in range(len(userContent_list_result)):
            try:
                if '동영상을 공유' in userContent_list_result[contntLength].text:
                    #print(contntLength + 1, '.', userContent_list_result[contntLength].text)
                    prfl_vodCnt += 1

                if '사진을 공유' in userContent_list_result[contntLength].text:
                    #print(contntLength + 1, '.', userContent_list_result[contntLength].text)
                    prfl_picCnt += 1

            except TimeoutException as ex:
                print('Timeout Exception', ex)
                break

            contentCnt +=1

        print('동영상수 :', prfl_vodCnt)
        print('사진수 :', totalPicCnt)
        print('게시글(사진, 동영상 포함) 수 : ', len(userContent_list_result))
        print('게시글(사진, 동영상 포함) 수 : ', contentCnt + totalPicCnt)
        print('게시글(텍스트로만 구성) 수 : ', contentCnt - (prfl_picCnt + prfl_vodCnt))


        if totalPicCnt >= 500:
            print('사진 수가 500장 이상일 경우 50점이 가산됩니다.')
            m_score_count_detail += 60
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)
        elif 200 <= totalPicCnt < 500:
            print('사진 수가 200장 이상 500장 미만일 경우 25점이 가산됩니다.')
            m_score_count_detail += 40
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)
        elif 10 <= totalPicCnt < 200:
            print('사진 수가 10장 이상 200장 미만일 경우 15점이 가산됩니다.')
            m_score_count_detail += 20
            m_score_count += m_score_count_detail
            # print("%%", m_score_count)

        ResultDict.update({'동영상수':prfl_vodCnt, '사진수':totalPicCnt })

        mScoreCount = m_score_count

        # 게시글 텍스트 크롤링
        autoScrollerContentsText(user_fbpage_url, driver)

        print('최종 T SCORE : ', tScoreCount)
        print('최종 C SCORE : ', cScoreCount)
        print('최종 M SCORE : ', mScoreCount)
        print()

        ResultDict.update({'T_SCORE':tScoreCount, 'C_SCORE':cScoreCount, 'M_SCORE':mScoreCount})

        print('최종 RESULT : ', ResultDict)

        print('requestClient :', requestClient)

        if requestClient == 'sci':
            #DB insert
            try:

                # Server Connection to MySQL:
                databaseConnection = mysqlConnection.DatabaseConnection_origin()
                databaseConnection.insert_record_origin_version(
                                                                ResultDict['사용자이름'],
                                                                ResultDict['페이스북페이지ID'],
                                                                ResultDict['전체기본정보'],
                                                                ResultDict['전체연락처정보'],
                                                                ResultDict['웹사이트및소셜링크정보'],
                                                                ResultDict['소개글'],
                                                                str(ResultDict['프로필게시개수']),
                                                                ResultDict['전체프로필정보'],
                                                                str(ResultDict['친구수']),
                                                                str(ResultDict['좋아요__사람전체명수']),
                                                                str(ResultDict['좋아요(image)__표시전체갯수']),
                                                                str(ResultDict['동영상수']),
                                                                str(ResultDict['사진수']),
                                                                str(ResultDict['T_SCORE']),
                                                                str(ResultDict['C_SCORE']),
                                                                str(ResultDict['M_SCORE']))
            except Exception as e_maria:
                logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

        elif requestClient == 'jeniel':
            try:
                # Server Connection to MySQL:
                databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()

                #db에 insert 하는 값은 str 형식이어야 한다, LIST 형식 사용하면 안된다.
                databaseConnection_jeniel.insert_record_facebookInfo(
                    ResultDict['사용자이름'],
                    ResultDict['페이스북페이지ID'],
                    ResultDict['전체기본정보'],
                    detailInfoList.replace(".", ""),
                    str(ResultDict['T_SCORE']),
                    str(ResultDict['C_SCORE']),
                    str(ResultDict['M_SCORE'])

                )


            except Exception as e_maria:
                logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))

        returnedValue_TCMCountGen = True

    else:
        print('M SCORE를 산출할 수 없습니다.')
        ResultDict.update({'T_SCORE': tScoreCount, 'C_SCORE': cScoreCount, 'M_SCORE': 0})

        try:
            # Server Connection to MySQL:
            databaseConnection_jeniel = mysqlConnection_jeniel.DatabaseConnection_jeniel()
            databaseConnection_jeniel.insert_record_facebookInfo(
                ResultDict['사용자이름'],
                ResultDict['페이스북페이지ID'],
                ResultDict['전체기본정보'],
                detailInfoList.replace(".", ""),
                str(ResultDict['T_SCORE']),
                str(ResultDict['C_SCORE']),
                str(ResultDict['M_SCORE'])
            )


        except Exception as e_maria:
            logger.error('[ Error ] MariaDB About information Insertion => {}'.format(e_maria))




        returnedValue_TCMCountGen = True

    print('returnedValue_TCMCountGen :', returnedValue_TCMCountGen)

    returnTCMResult = {}
    returnTCMResult['trueOrFalse'] = returnedValue_TCMCountGen
    returnTCMResult['tcmScore'] = ResultDict


    '''

    # 20180509 _0510
    # 가공 데이터 CSV 파일화 작업
    currDate = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
        time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(
        time.localtime().tm_sec)

    with open("C:\\python_project\\aster879_project\\PycharmProjects\\CrawledData_"+ hereWork +"_" + currDate + ".csv",
            "w", newline='', encoding='utf8') as fbFile:

        # 20180509
        writer = csv.writer(fbFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([str(user_fbpage_url + '님의 페이스북 정보 근거 TCM 산출 정보')])

        for key, val in ResultDict.items():
            writer.writerow([key, val])

        writer.writerow([])

    # 20180509
    #생성한 CSV 파일 읽기 - 정상 입력 검사
    with open("C:\\python_project\\aster879_project\\PycharmProjects\\CrawledData_"+ hereWork +"_" + currDate + ".csv", "r", encoding='utf8') as readCSVfile:
        reader = csv.reader(readCSVfile)
        # read file row by row
        for row in reader:
            print(row)

    '''


    return returnTCMResult



def autoScrollerUserWrapperContents(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 3):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup_html = bs(autoScrolled_data, 'html.parser')
        userContent_list_result = []

    try:
        time.sleep(2)
        userContent_list_result = autoScrolled_data_soup_html.find_all('div', attrs={'class': 'userContentWrapper'})

    except Exception as e:
        print('autoScrollerUserWrapperContents에서 userContentWrapper를 찾지 못했습니다. -> ', e)
        #userContent_list_result is None
        userContent_list_result = None

    return userContent_list_result




def autoScroller_MSCORE(User_site_url_addr, driver):
    driver.get(User_site_url_addr + '/photos_albums')

    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    last_height = driver.execute_script("return document.body.scrollHeight")

    userContent_list_result = []

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 5):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup = bs(autoScrolled_data, 'html.parser')
        try:

            userContent_list_result = autoScrolled_data_soup.find_all('span', attrs={'class': '_2ieq _50f7'})
        except:
            print('해당 클래스 값이 없습니다.')

    pictureCntT = 0
    pictureCnt = 0
    for picture_index in userContent_list_result:
        pictureDiscribText = picture_index.text.split(' · ')

        matching = [s for s in pictureDiscribText if "항목" in s]
        pictureCnt = int(str(matching).split()[1].split('개')[0])

        pictureCntT += pictureCnt
    print('총 사진 수 : ', pictureCntT)

    return pictureCntT



#autoScroller관련 함수 =========================================================================

#상단에 인코딩을 명시적으로 표시해 줄 것 참조 : https://kyungw00k.github.io/2016/04/08/python-%ED%8C%8C%EC%9D%BC-%EC%83%81%EB%8B%A8%EC%97%90-%EC%BD%94%EB%93%9C-%EB%82%B4-%EC%9D%B8%EC%BD%94%EB%94%A9%EC%9D%84-%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9C%BC%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%A0-%EA%B2%83/
def autoScroller(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 3):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup_html = bs(autoScrolled_data, 'html.parser')

    #return bs(autoScrolled_data, 'html.parser')
    return autoScrolled_data_soup_html



def autoScrollerContentsText(User_timeLine_site_url_addr, driver):

    driver.get(User_timeLine_site_url_addr)
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    textDataList = []
    autoScrolled_data_soup = ''
    for cyc in range(0, 10):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data = driver.page_source
        autoScrolled_data_soup = bs(autoScrolled_data, 'html.parser')

    try:
        userContent_list_result = autoScrolled_data_soup.find_all('div',attrs={'class': '_5pbx userContent _3576'})
        #print('@@', userContent_list_result)
        for textOnly in userContent_list_result:
            textData = textOnly.text.split()
            textDataList += textData
        print('textDataList :', textDataList)
        textDataListVal = ''
        corp_cnt = 0

        try:
            if '엘지' in textDataList:
                print('엘지(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '현대' in textDataList:
                print('현대(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '기아' in textDataList:
                print('기아(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '삼성' in textDataList:
                print('삼성(이)라는 글자가 노출되었습니다.')
                corp_cnt += 7
                textDataListVal += textDataList

            if '에스케이' in textDataList:
                print('에스케이(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '한국' in textDataList:
                print('한국(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '케이티' in textDataList:
                print('케이티(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '지에스' in textDataList:
                print('지에스(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '신한' in textDataList:
                print('신한(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '하나' in textDataList:
                print('하나(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '한화' in textDataList:
                print('한화(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '우리' in textDataList:
                print('우리(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '대우' in textDataList:
                print('대우(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '두산' in textDataList:
                print('두산(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '롯데' in textDataList:
                print('롯데(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '케이비' in textDataList:
                print('케이비(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '흥국' in textDataList:
                print('흥국(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '기업' in textDataList:
                print('기업(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if 'S-oil' in textDataList:
                print('s-oil(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '대한' in textDataList:
                print('대한(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '아시아나' in textDataList:
                print('아시아나(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '동국' in textDataList:
                print('동국(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '코오롱' in textDataList:
                print('코오롱(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '네이버' in textDataList:
                print('네이버(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '다음' in textDataList:
                print('다음(이)라는 글자가 노출되었습니다')
                corp_cnt += 7
                textDataListVal += textDataList

            if '사원' in textDataList:
                print('사원증(이)라는 글자가 노출되었습니다.')
                corp_cnt += 7
                textDataListVal += textDataList

            print(corp_cnt)
            print('textDataListVal', textDataListVal)
            #readCSV(textDataListVal)

        except Exception as es:
            print('기업 이름이 검색되지 않았습니다. : ', es)

    except Exception as readCsvEx:
        print('AutoCrolling 한 객체가 없습니다. ')



#CSV 파일 읽기 ======================================================================
def readCSV(searchTValue):

    #C:\python_project\aster879_project\PycharmProjects
    reader = csv.reader(
        open('C:\\python_project\\aster879_project\\PycharmProjects\\1_500Corp.csv', 'rt', encoding='utf-8-sig', newline=''), delimiter=' ', quotechar='|')

    print(searchTValue)

    corpList = []
    for row in reader:
        corpList.append(', '.join(row))

    returnScore = 0
    #500대 기업 loop
    for row2 in corpList:
        returnScore1 = 0
        for loopInt in range(len(searchTValue)):
            print('searchTValue['+str(loopInt)+'] :', searchTValue[loopInt])
            if searchTValue[loopInt] in row2:
                returnScore1 += 10
                break
        returnScore += returnScore1
    print(returnScore)
    return returnScore

