#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import logging.handlers
from aster_dev_201808.aster879.worknet_just import mysqlConnection_just as mySQL_conn


# class worknetCrawlerBot:
#     def __init__(self):
#         logger.debug('start')
#         print('worknet crawling start')

global driver
global user_id
global user_pass
global pagelet_dict_data
global t_score_count
global returnValue_facebook

global hereWork
hereWork = 'worknet'

currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
    time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

logger = logging.getLogger(hereWork+'_logging')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

file_max_bytes = 10*1024*1024   # log file size : 10MB
fileHandler = logging.handlers.RotatingFileHandler('C:\\dev_tenspace\\PycharmProjects\\log\\' + hereWork + '_crawlerbot_logging_' + currTime, maxBytes=file_max_bytes, encoding='UTF-8', backupCount=10)
streamHandler = logging.StreamHandler()

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(fileHandler)

start_time_all = time.time()
returnValue_worknet = False

def autoScroller(driver):
    SCROLL_PAUSE_TIME = 0.5

    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        last_height = new_height

    autoScrolled_data_soup_html = bs(driver.page_source, 'html.parser')

    return autoScrolled_data_soup_html

def getTotalRecruitCount(driver):
    worknet_firstPage_soup_html = bs(driver.page_source, 'html.parser')
    logger.debug('게시글 전체 갯수 : {}'.format(worknet_firstPage_soup_html.select("#searchCondExtVO > div.sub_search_wrap.matching2 > div.sch_total > span > em")[0].text))

    totCnt_recruit = worknet_firstPage_soup_html.select("#searchCondExtVO > div.sub_search_wrap.matching2 > div.sch_total > span > em")[0].text.replace(",", "")

    print('전체 게시글 개수:',totCnt_recruit)

    return totCnt_recruit

def couldScrolling(driver):
    ScrollTestResult = False

    try:
        driver.execute_script("return document.body.scrollHeight")

        print('스크롤이 가능한 페이지 입니다.')
        logger.debug('스크롤이 가능한 페이지 입니다.')

        ScrollTestResult = True

    except Exception as e_expArticle:
        print('스크롤이 불가능한 페이지 입니다.', e_expArticle)
        logger.error('스크롤이 불가능한 페이지 입니다. : {}'.format(e_expArticle) )

    return ScrollTestResult


def getPagination(driver, searchURL):
    page_url = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?pageIndex={}"
    driver.get(page_url.format(1))
    totalCount_str = getTotalRecruitCount(driver)
    totalCount_page = int(int(totalCount_str)/10) + 1

    logger.debug('전체 페이지 수: {}'.format(totalCount_page))
    print('전체 페이지 수:', totalCount_page)

    dept_page_url = [page_url.format(i) for i in range(1, 3)]
    result_workNetDictionaty = {}

    #데이터베이스에 연결
    database_connection = mySQL_conn.DatabaseConnection_jeniel()
    returnedselectDataList = database_connection.select_record()

    i = 0
    #insertCnt = 0
    for page_length in range(len(dept_page_url)):

        insertCnt = 1
        try:
            driver.get(dept_page_url[i])

            i += 1
            logger.debug('current_url => {}'.format(driver.current_url))
            result_autoScroller = autoScroller(driver)

            #각 공고별 정보 검색 및 취득
            for list_length in range(len(result_autoScroller.select("#searchCondExtVO > table > tbody > tr"))):
                print('각 공고별 검색 start')
                #기업 명 체크박스 선별
                #pageSourceText = result_autoScroller.find_all('input', {'id': 'chkboxWantedAuthNo' + list_indies.split(',')[list_length]} )

                #마감된 채용정보 alert 발생 시 error 발생하는 try 문
                try:
                    corpJobText = result_autoScroller.select("#list" + str(list_length + 1) + " > td:nth-of-type(3) > dl > dt > a")[0].text

                    corpJobText_URL = result_autoScroller.find("a", string=corpJobText)

                    #하단의 공고 세부항목으로 진입 후 출력되는 공고 제목과 비교하기 위함.
                    corpJboArticleTitle = corpJobText.replace("	", " ").replace(" ", " ").replace("    ", " ").replace(
                        "        ", " ").replace("\n", "").replace("\xa0", "")

                    #각 구인 공고별 URL 취득
                    corpJobText_detail_URL = corpJobText_URL['href']


                    # Maria-Field : 구인인증번호(구인공고고유값) : articleUniqueNum
                    articleOverViewInfo = result_autoScroller.find(id='chkboxWantedAuthNo' + str(list_length))['value']
                    logger.debug('구인인증번호|회사명|공고내용: {}'.format(articleOverViewInfo))
                    print()

                    # Maria-Field : articleUniqueNum
                    # Maria-Data : articleUniqueNum
                    articleUniqueNum = articleOverViewInfo.split('|')[0]


                    #구인인증 번호 취득 후, DB에서 articleUniqueNum만 받은 list와 값 비교를 하여 존재하는 값이면 다음 과정을 진행하지 않고,
                    #존재하지 않는 값이면 다음 과정을 진행하도록 함.

                    print('구인인증번호 값 : ', articleUniqueNum)

                    #기 크롤링한 구인공고는 크롤링하지 않는다.
                    if articleUniqueNum in returnedselectDataList:
                        print('기 크롤링한 구인공고임.')
                        logger.debug('기 크롤링한 구인공고임. 구인인증번호: {}'.format(articleUniqueNum))
                        continue

                    #한번도 크롤링 하지 않은 구인공고 정보를 가져온다.
                    #DB Insert가 실패하더라도 이는 기존의 공고라기 보다는 크롤링 과정 중 발생하는 중복에 의해 insert가 실패한 것이다.
                    else:
                        print('처음 크롤링하는 구인 공고임.')
                        # Maria-Field : corpNm
                        # Maria-Data : corpNm
                        corpNm = articleOverViewInfo.split('|')[1]

                        # Maria-Field : corpWantJob
                        # Maria-Data : corpWantJob
                        corpWantJob = articleOverViewInfo.split('|')[2]

                        # DATA : 구인인증번호: articleUniqueNum / 회사명: corpNm / 공고내용: corpWantJob
                        result_workNetDictionaty['구인인증번호_'+articleUniqueNum] = articleUniqueNum
                        result_workNetDictionaty['회사명_'+articleUniqueNum] = corpNm
                        result_workNetDictionaty['공고제목_' + articleUniqueNum] = corpWantJob

                        #구인 인증번호를 DB 검색하여 존재하는 인증번호이면 정보 취득 skip : 구인인증번호 SELECT 하여 이 값을 list로 만들고, 이를 가지고 기존 구인인증번호인지를 검색할 예정.

                        #No.1 세부 공고 내부로 진입
                        driver.get('http://www.work.go.kr'+corpJobText_detail_URL)

                        returnedPossibleScroll = couldScrolling(driver)
                        print('return Scroll Test result: ', returnedPossibleScroll)

                        #Scroll Test Success
                        if returnedPossibleScroll == True:

                            corpJobDetailArticle = autoScroller(driver)

                            # Maria-Field : 공고 제목 : corpRecruitArticleTitle
                            # Maria-Data : corpRecruitArticleTitle
                            corpRecruitArticleTitle = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(3) > h3')[0].text.replace("	","").replace(" ", "").replace("    ", "").replace("        ", "").replace("\n", "").replace("\xa0", "").split("이메일입사지원")[0]

                            # DATA : corpRecruitArticleTitle
                            result_workNetDictionaty['공고제목상세_' + articleUniqueNum] = corpRecruitArticleTitle

                            #공고 리스트 제목과 세부 공고 제목의 일치 여부 검증
                            if corpRecruitArticleTitle == corpJboArticleTitle:
                                logger.debug('공고 리스트 제목과 세부 공고 제목간 Text 일치')

                                # Maria-Field : 조회수 : searchArticleCnt
                                searchArticleCntTitle = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(3) > p > b:nth-of-type(1)')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")

                                # Maria-Data : 조회수 '숫자'
                                searchArticleCnt = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(3) > p')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "").split("|")[0].split(searchArticleCntTitle)[1].split("명")[0]

                                # DATA : searchArticleCnt
                                result_workNetDictionaty[searchArticleCntTitle + '_' + articleUniqueNum] = searchArticleCnt

                                # Maria-Field : '지원자' : articleApplyCnt
                                applicantArticleCntTitle = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(3) > p > b:nth-of-type(2)')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")

                                # Maria-Data : 지원자 '숫자'
                                applicantArticleCnt = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(3) > p')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "").split("|")[1].split(applicantArticleCntTitle)[1].split("명")[0]

                                # DATA : articleApplyCnt
                                result_workNetDictionaty[applicantArticleCntTitle + '_'+ articleUniqueNum] = applicantArticleCnt
                                logger.debug('{}:{}명, {}:{}명'.format(searchArticleCntTitle, int(searchArticleCnt), applicantArticleCntTitle, int(applicantArticleCnt)))

                                #회사 상세 정보
                                #회사 로고 img directory
                                #Maria-Field : 회사 이미지 사용 유무 : corpImageYN(boolean)
                                corpImgDir = corpJobDetailArticle.find(id='logoImg')['src']
                                if 'none_imglogo.gif' in corpImgDir:
                                    logger.debug('회사 이미지 사용하지 않음')
                                    result_workNetDictionaty['corpImgDir_' + articleUniqueNum] = ''
                                else:
                                    #Maria-Data : corpImgDir
                                    logger.debug('회사 이미지 저장 디렉토리 : {}'.format(corpImgDir))
                                    result_workNetDictionaty['corpImgDir_' + articleUniqueNum] = corpImgDir

                                #회사 소개 상세 정보(회사명, 대표자명, 근로자수, 자본금, 연매출액,
                                # 업종, 주요사업내용, 회사주소, 홈페이지)
                                detailCorpInfo_length = len(corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr'))

                                # 회사 소개 항목을 덜 채운 상태임.
                                if detailCorpInfo_length == 7:

                                    #회사 소개 항목을 모두 채운 상태임.
                                    #detailCorpInfo_length 자체가 len()의 결과물이기 때문에 다시 len()으로 감싸놓을 필요 없음.
                                    for tr_length in range(detailCorpInfo_length):
                                        trUnderThLen = len(corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type('+ str(tr_length + 1) +') > th'))

                                        for thORtd_length in range(trUnderThLen):

                                            # Maria-Filed :
                                            # 회사명: corpNm_detl/대표자명: ceoNm/근로자수: workerCnt/ 자본금: jabon/
                                            # 연매출액: yearIncome/업종: jobKind/주요사업내용: jobKind_main/회사주소:corpAddr
                                            # 홈페이지: homepage
                                            detailPartTitle = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(tr_length + 1) + ') > th:nth-of-type(' + str(thORtd_length + 1) + ')')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")
                                            detailPartContent = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(tr_length + 1) + ') > td:nth-of-type(' + str(thORtd_length + 1) + ')')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "").replace("-", "")

                                            # DATA : corpNm_detail ~ homepage
                                            result_workNetDictionaty[detailPartTitle + '_' + articleUniqueNum] = detailPartContent
                                            logger.debug('{}-{}.{}:{}'.format(tr_length, thORtd_length, detailPartTitle,detailPartContent))

                                else:
                                    #print('detailCorpInfo_length가 7이 아닙니다.')
                                    if detailCorpInfo_length == 0:
                                        logger.debug('회사 소개가 없습니다.')
                                    else:
                                        logger.debug('회사 소개 tr 갯수 : {}'.format(detailCorpInfo_length))

                                #Maria-Field :
                                #회사 공고 지원자 숙지 사항(지원자격, 근무조건, 고용형태)
                                alertApplicant_len = len(corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li'))
                                #print('@', alertApplicant_len)
                                for alert_length in range(alertApplicant_len):
                                    alertNoticeTitle = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(alert_length + 1) + ') > strong')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")

                                    #지원자격, 근무조건, 고용형태(타이틀)
                                    logger.debug('#{}'.format(alertNoticeTitle) )
                                    alertNoticecontent_len = len(corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(alert_length + 1) + ') > dl > dt'))

                                    for alterNotice_length in range(alertNoticecontent_len):
                                        #지원자격: applyRequire/근무조건: workCondition/고용형태: hireType 각각의 세부항목
                                        articleNoticeDetailTitle = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(alert_length + 1) + ') > dl > dt:nth-of-type('+ str( alterNotice_length+1 ) +')')[0].text.replace("	", "").replace(" ", "").replace("    ", "").replace("        ", "").replace("\n","").replace("\xa0", "")
                                        articleNoticeDetailContent = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(alert_length + 1) + ') > dl > dd:nth-of-type('+ str( alterNotice_length+1 ) +')')[0].text.replace("	", "").replace(" ", "").replace("    ", "").replace("        ", "").replace("\n","").replace("\xa0", "").replace("-", "")

                                        # DATA : applyRequire ~ hireType
                                        result_workNetDictionaty[articleNoticeDetailTitle + '_' + articleUniqueNum] = articleNoticeDetailContent

                                #복리후생
                                #welfare_len = len(corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(2) span > img'))
                                #corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(2) span > img:nth-of-type(' +  + ')')
                                #복리후생 조건을 img 테그의 alt 값으로 설정하여 다른 이미지 지정하는 방식임. 특별한 키값이 존재하는 것이 아니라서 감지하기 어려움.

                                #기업 홍보 존
                                #corpJobDetailArticle.select('div#corpInfoView > div#extCoinfo > iframe#corpInfo > ')
                                #iframe을 잡아야 함.

                                #Maria-Field : 모집요강제목: mojibYoGangTitle/ 구인인증번호: mojibYoGangSerialNo
                                mojibYoGangTitle = corpJobDetailArticle.select('div.empdetail > h4')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")
                                mojibYoGangSerialNo = corpJobDetailArticle.select('div.empdetail > font')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")

                                #기업 홍보존 하단의 6개 테이블 출력 부분 : 모집요강, 근무조건, 전형방법, 우대사항, 기타사항, 채용담당자

                                #모집요강 구인인증번호 출력
                                logger.debug('{} {}'.format(mojibYoGangTitle, mojibYoGangSerialNo))
                                lengthOfTable = len(corpJobDetailArticle.select('div.empdetail > table.info_list'))
                                print()
                                logger.debug('$$: {}'.format(lengthOfTable))
                                print()

                                for infoTable_length in range(lengthOfTable):
                                    print()
                                    logger.debug('infoTable_No{}'.format(str(infoTable_length + 1)) )
                                    #Maria-Field :
                                    infoTableTitle = corpJobDetailArticle.select('div.empdetail > table:nth-of-type('+ str(infoTable_length +1) +') > caption')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")

                                    logger.debug('-{}'.format(corpJobDetailArticle.select('div.empdetail > table:nth-of-type('+ str(infoTable_length +1) +') > caption')[0].text.replace(
                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")) )

                                    length_table_content = len(corpJobDetailArticle.select('div.empdetail > table:nth-of-type('+ str(infoTable_length +1) +') > tbody > tr'))
                                    #nth-of-type()를 적용시키기 위해서는 class 명을 명시하지 말고 nth-of-type을 적용하여야 한다.

                                    print()
                                    logger.debug('{} : {}'.format(infoTableTitle, length_table_content) )

                                    if length_table_content == 1:
                                        try:
                                            infoTableContent_title = corpJobDetailArticle.select(
                                                'div.empdetail > table:nth-of-type(' + str(
                                                    infoTable_length + 1) + ') > thead > tr > th')[0].text.replace(
                                                "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n", "").replace("\xa0", "")

                                            infoTableContent_contents = corpJobDetailArticle.select(
                                                'div.empdetail > table:nth-of-type(' + str(
                                                    infoTable_length + 1) + ') > tbody > tr > td')[0].text.replace(
                                                "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n", "").replace("\xa0", "").replace("-", "")

                                            result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                                            print(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum])
                                            logger.debug('{}'.format(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]))

                                        except Exception as e_etc:
                                            print('이런 경우는 없어야 함. ', e_etc)

                                            infoTableContent_title = '더추가할구인조건'

                                            infoTableContent_contents = corpJobDetailArticle.select(
                                                'div.empdetail > table:nth-of-type(' + str(
                                                    infoTable_length + 1) + ') > tbody > tr > td')[0].text.replace(
                                                "	", " ").replace(" ", " ").replace("    ", " ").replace("        ",
                                                                                                         " ").replace("\n",
                                                                                                                     " ").replace(
                                                "\xa0", "").replace("-", "")

                                            result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                                            logger.debug('{}'.format(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]) )

                                    elif length_table_content == 3:
                                        print('회사 주소 및 지도 표시')
                                        for infoTable_content_length in range(length_table_content - 1):
                                            logger.debug('infoTable_content_No.{}'.format(str(infoTable_content_length + 1)) )
                                            # Maria-Field :
                                            try:
                                                infoTableContent_title = corpJobDetailArticle.select(
                                                    'div.empdetail > table:nth-of-type(' + str(
                                                        infoTable_length + 1) + ') > thead > tr > th')[0].text.replace(
                                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n", "").replace("\xa0", "")

                                                infoTableContent_contents = corpJobDetailArticle.select(
                                                    'div.empdetail > table:nth-of-type(' + str(
                                                        infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                                        infoTable_content_length + 1) + ') > td')[0].text.replace(
                                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n", "").replace("\xa0", "").replace("-", "")

                                                result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                                                logger.debug('{}'.format(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]) )

                                            except Exception as e_etc:
                                                print('thead 태그가 없는 경우가 대부분임 : ', e_etc)
                                                infoTableContent_contents = corpJobDetailArticle.select(
                                                    'div.empdetail > table:nth-of-type(' + str(
                                                        infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                                        infoTable_content_length + 1) + ') > td')[0].text.replace(
                                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        "," ").replace("\n","").replace("\xa0", "").replace("-", "")

                                                result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                                                logger.debug('{}'.format(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]) )

                                    else:
                                        for infoTable_content_length in range(length_table_content):
                                            print('infoTable_content_No.', str(infoTable_content_length + 1))
                                            # Maria-Field :
                                            try:
                                                infoTableContent_title = corpJobDetailArticle.select(
                                                    'div.empdetail > table:nth-of-type(' + str(
                                                        infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                                        infoTable_content_length + 1) + ') > th')[0].text.replace(
                                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        "," ").replace("\n", "").replace("\xa0", "")

                                                infoTableContent_contents = corpJobDetailArticle.select(
                                                    'div.empdetail > table:nth-of-type(' + str(
                                                        infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                                        infoTable_content_length + 1) + ') > td')[0].text.replace(
                                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        "," ").replace("\n", "").replace("\xa0", "").replace("-", "")

                                                result_workNetDictionaty[
                                                    infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                                                logger.debug('{}'.format(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]) )

                                            except Exception as e_th:
                                                print('기타사항 테이블 진입 : th 태그가 없음', e_th)

                                                infoTableContent_title = '더추가할구인조건'

                                                infoTableContent_contents = corpJobDetailArticle.select(
                                                    'div.empdetail > table:nth-of-type(' + str(
                                                        infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                                        infoTable_content_length + 1) + ') > td')[0].text.replace(
                                                    "	", " ").replace(" ", " ").replace("    ", " ").replace("        ",
                                                                                                             " ").replace(
                                                    "\n",
                                                    "").replace(
                                                    "\xa0", "").replace("-", "")

                                                result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                                                logger.debug('{}'.format(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]) )


                                        #Maria-Field :
                                        #모집요강= 모집직종:recruitJobKind / 직종키워드:jobKindKeyword / 관련직종:relatedJobKind / 직무내용:whatWork
                                        #          경력조건:experOpt / 학력:eduCond / 고용형태:hireType_detl / 모집인원:hireCnt / 근무예정지:workPlace/ 소속산업단지:industCommnt / 인근전철역:nearSubway
                                        #근무환경및복리후생: 임금조건: wageCond/ 식사(비)제공: mealOffer/ 근무시간: workTime/ 근무형태: jobType/ 사회보험: Socialensure/ 퇴직금지급방법: retirePay
                                        #전형방법: 접수마감일: applyDueDate/ 전형방법: howToRecruit_detl/ 접수방법: howToApply_detl/ 제출서류준비물: applyDoc/ 제출서류양식 첨부: appliDocAttach
                                        #우대사항: 외국어능력: bilingual/ 전공: collgMajor/ 자격면허: license/ 컴퓨터활용능력: comCap/ 우대조건: prfrFactor_detl
                                        #          병역특례채용희망: wishHireMil/ 장애인채용희망: wishHireDisabled/ 기타우대사항: etcPrefer/ 복리후생: welfare/ 장애인편의시설: facltDisabled
                                        #기타입력사항: 더추가할구인조건: moreHireCond

                                        # DATA : recruitFactors, workEnv_welfare, howtoapply, preferFactor, etc
                                        result_workNetDictionaty[infoTableContent_title + '_'+ articleUniqueNum] = infoTableContent_contents
                                        logger.debug('#{},{}'.format(infoTableContent_title, result_workNetDictionaty[infoTableContent_title + '_'+ articleUniqueNum]) )

                                        logger.debug('{}:{}'.format(infoTableContent_title, infoTableContent_contents))
                                        #End of Loop

                                #채용담당자
                                recruitManagerTitle = corpJobDetailArticle.select('div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > caption')[0].text.replace(
                                "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "")

                                length_recruitManagerInfo = len(corpJobDetailArticle.select('div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > tbody > tr'))

                                for recruitMngInf_len in range(length_recruitManagerInfo):
                                    recruitManagerDetailTitle = corpJobDetailArticle.select(
                                        'div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > tbody > tr:nth-of-type('+ str(recruitMngInf_len + 1) +') > th')[0].text.replace(
                                "	", " ").replace(" ", " ").replace("    ", " ").replace("        ", " ").replace("\n","").replace("\xa0", "").replace("/", "-")

                                    recruitManagerDetailContents = corpJobDetailArticle.select(
                                        'div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(recruitMngInf_len + 1) + ') > td')[0].text.replace(
                                        "	", " ").replace(" ", " ").replace("    ", " ").replace("        "," ").replace("\n","").replace("\xa0", "").replace("/", "_")
                                    print('인사담당자이메일:', recruitManagerDetailContents)

                                    # DATA : 부서/담당자: recruitMngr / 전화번호: recruitMngrTel1 / 휴대전화: recruitMngrTel2/ 팩스번호: faxNo / email: recruitMngrEmail
                                    result_workNetDictionaty[recruitManagerDetailTitle + '_' + articleUniqueNum] = recruitManagerDetailContents
                                    logger.debug('{}:{}'.format(recruitManagerDetailTitle, recruitManagerDetailContents))


                                #Test print
                                logger.debug('DB INSERT : '
                                             '{},{},{},{},{},{},{},{},{},{},'
                                             '{},{},{},{},{},{},{},{},{},{},'
                                             '{},{},{},{},{},{},{},{},{},{},'
                                             '{},{},{},{},{},{},{},{},{},{},'
                                             '{},{},{},{},{},{},{},{},{},{},'
                                             '{},{},{},{},{},{}'.format(
                                        result_workNetDictionaty['구인인증번호_' + articleUniqueNum],  # articleUniqueNum
                                        result_workNetDictionaty['회사명_' + articleUniqueNum],  # corpNm
                                        result_workNetDictionaty['공고제목_' + articleUniqueNum],  # corpWantJob
                                        result_workNetDictionaty['공고제목상세_' + articleUniqueNum],  # corpRecruitArticleTitle
                                        result_workNetDictionaty['조회수_' + articleUniqueNum],  # searchArticleCnt
                                        result_workNetDictionaty['지원자_' + articleUniqueNum],  # applicantArticleCnt
                                        result_workNetDictionaty['corpImgDir_' + articleUniqueNum],  # corpImgDir
                                        result_workNetDictionaty['회사명_' + articleUniqueNum],  # corpNm_detl
                                        result_workNetDictionaty['대표자명_' + articleUniqueNum],  # ceoNm
                                        result_workNetDictionaty['근로자수_' + articleUniqueNum],  # workerCnt
                                        result_workNetDictionaty['자본금_' + articleUniqueNum],  # jabon
                                        result_workNetDictionaty['연매출액_' + articleUniqueNum],  # yearIncome
                                        result_workNetDictionaty['업종_' + articleUniqueNum],  # jobKind
                                        result_workNetDictionaty['주요사업내용_' + articleUniqueNum],# jobKind_main
                                        result_workNetDictionaty['회사주소_' + articleUniqueNum],  # corpAddr
                                        result_workNetDictionaty['홈페이지_' + articleUniqueNum],  # homepage
                                        result_workNetDictionaty['모집직종_' + articleUniqueNum],  # recruitJobKind
                                        result_workNetDictionaty['직종키워드_' + articleUniqueNum],  # jobKindKeyword
                                        result_workNetDictionaty['관련직종_' + articleUniqueNum],  # relatedJobKind
                                        result_workNetDictionaty['직무내용_' + articleUniqueNum],  # whatWork
                                        result_workNetDictionaty['경력조건_' + articleUniqueNum],  # experOpt
                                        result_workNetDictionaty['학력_' + articleUniqueNum],  # eduCond
                                        result_workNetDictionaty['근무지역_' + articleUniqueNum],  # workArea
                                        result_workNetDictionaty['임금_' + articleUniqueNum],  # wageCond
                                        result_workNetDictionaty['고용형태_' + articleUniqueNum],  # hireType_detl
                                        result_workNetDictionaty['모집인원_' + articleUniqueNum],  # hireCnt
                                        result_workNetDictionaty['근무예정지_' + articleUniqueNum],  # workPlace
                                        result_workNetDictionaty['소속산업단지_' + articleUniqueNum],  # industCommnt
                                        result_workNetDictionaty['인근전철역_' + articleUniqueNum],
                                        result_workNetDictionaty['임금조건_' + articleUniqueNum],  # wageCond_detl
                                        result_workNetDictionaty['식사(비)제공_' + articleUniqueNum],  # mealOffer
                                        result_workNetDictionaty['근무시간_' + articleUniqueNum],  # workTime
                                        result_workNetDictionaty['근무형태_' + articleUniqueNum],  # jobType
                                        result_workNetDictionaty['사회보험_' + articleUniqueNum],
                                        result_workNetDictionaty['퇴직금지급방법_' + articleUniqueNum],
                                        result_workNetDictionaty['접수마감일_' + articleUniqueNum],  # applyDueDate
                                        result_workNetDictionaty['전형방법_' + articleUniqueNum],  # howToRecruit_detl
                                        result_workNetDictionaty['접수방법_' + articleUniqueNum],  # howToApply_detl
                                        result_workNetDictionaty['제출서류준비물_' + articleUniqueNum],
                                        result_workNetDictionaty['제출서류양식첨부_' + articleUniqueNum],  # applyDocAttach
                                        result_workNetDictionaty['외국어능력_' + articleUniqueNum],  # bilingual
                                        result_workNetDictionaty['전공_' + articleUniqueNum],  # collgMajor
                                        result_workNetDictionaty['자격면허_' + articleUniqueNum],  # license
                                        result_workNetDictionaty['컴퓨터활용능력_' + articleUniqueNum],  # comCap
                                        result_workNetDictionaty['우대조건_' + articleUniqueNum],  # prfrFactor_detl
                                        result_workNetDictionaty['병역특례채용희망_' + articleUniqueNum],  # wichHireMil
                                        result_workNetDictionaty['장애인채용희망_' + articleUniqueNum],  # wishHireDisabled
                                        result_workNetDictionaty['기타우대사항_' + articleUniqueNum],  # etcPrefer
                                        result_workNetDictionaty['복리후생_' + articleUniqueNum],
                                        result_workNetDictionaty['장애인편의시설_' + articleUniqueNum],  # facltDisabled
                                        result_workNetDictionaty['더추가할구인조건_' + articleUniqueNum],  # moreHireCond
                                        result_workNetDictionaty['부서-담당자_' + articleUniqueNum],  # recruitMngr
                                        result_workNetDictionaty['전화번호_' + articleUniqueNum],  # recruitMngrTel1
                                        result_workNetDictionaty['휴대전화_' + articleUniqueNum],  # recruitMngrTel2
                                        result_workNetDictionaty['팩스번호_' + articleUniqueNum],  # faxNo
                                        result_workNetDictionaty['E-mail_' + articleUniqueNum]  # recruitMngrEmail
                                    )
                                )

                                # DB INSERT
                                #print('DB_column_01: ', result_workNetDictionaty['구인인증번호_' + articleUniqueNum])  # articleUniqueNum
                                database_connection = mySQL_conn.DatabaseConnection_jeniel()
                                insertResult = database_connection.insert_new_record(
                                    result_workNetDictionaty['구인인증번호_' + articleUniqueNum],  # articleUniqueNum
                                    result_workNetDictionaty['회사명_' + articleUniqueNum],  # corpNm
                                    result_workNetDictionaty['공고제목_' + articleUniqueNum],  # corpWantJob
                                    result_workNetDictionaty['공고제목상세_' + articleUniqueNum],  # corpRecruitArticleTitle
                                    result_workNetDictionaty['조회수_' + articleUniqueNum],  # searchArticleCnt
                                    result_workNetDictionaty['지원자_' + articleUniqueNum],  # applicantArticleCnt
                                    result_workNetDictionaty['corpImgDir_' + articleUniqueNum],  # corpImgDir
                                    result_workNetDictionaty['회사명_' + articleUniqueNum],  # corpNm_detl
                                    result_workNetDictionaty['대표자명_' + articleUniqueNum],  # ceoNm
                                    result_workNetDictionaty['근로자수_' + articleUniqueNum],  # workerCnt
                                    result_workNetDictionaty['자본금_' + articleUniqueNum],  # jabon
                                    result_workNetDictionaty['연매출액_' + articleUniqueNum],  # yearIncome
                                    result_workNetDictionaty['업종_' + articleUniqueNum],  # jobKind
                                    result_workNetDictionaty['주요사업내용_' + articleUniqueNum],   # jobKind_main
                                    result_workNetDictionaty['회사주소_' + articleUniqueNum],  # corpAddr
                                    result_workNetDictionaty['홈페이지_' + articleUniqueNum],  # homepage
                                    result_workNetDictionaty['모집직종_' + articleUniqueNum],  # recruitJobKind
                                    result_workNetDictionaty['직종키워드_' + articleUniqueNum],  # jobKindKeyword
                                    result_workNetDictionaty['관련직종_' + articleUniqueNum],  # relatedJobKind
                                    result_workNetDictionaty['직무내용_' + articleUniqueNum],  # whatWork
                                    result_workNetDictionaty['경력조건_' + articleUniqueNum],  # experOpt
                                    result_workNetDictionaty['학력_' + articleUniqueNum],  # eduCond
                                    result_workNetDictionaty['근무지역_' + articleUniqueNum],  # workArea
                                    result_workNetDictionaty['임금_' + articleUniqueNum],  # wageCond
                                    result_workNetDictionaty['고용형태_' + articleUniqueNum],  # hireType_detl
                                    result_workNetDictionaty['모집인원_' + articleUniqueNum],  # hireCnt
                                    result_workNetDictionaty['근무예정지_' + articleUniqueNum],  # workPlace
                                    result_workNetDictionaty['소속산업단지_' + articleUniqueNum],  # industCommnt
                                    result_workNetDictionaty['인근전철역_' + articleUniqueNum],  # nearSubway
                                    result_workNetDictionaty['임금조건_' + articleUniqueNum],  # wageCond_detl
                                    result_workNetDictionaty['식사(비)제공_' + articleUniqueNum],  # mealOffer
                                    result_workNetDictionaty['근무시간_' + articleUniqueNum],  # workTime
                                    result_workNetDictionaty['근무형태_' + articleUniqueNum],  # jobType
                                    result_workNetDictionaty['사회보험_' + articleUniqueNum],  # socialEnsure
                                    result_workNetDictionaty['퇴직금지급방법_' + articleUniqueNum],  # retirePay
                                    result_workNetDictionaty['접수마감일_' + articleUniqueNum],  # applyDueDate
                                    result_workNetDictionaty['전형방법_' + articleUniqueNum],  # howToRecruit_detl
                                    result_workNetDictionaty['접수방법_' + articleUniqueNum],  # howToApply_detl
                                    result_workNetDictionaty['제출서류준비물_' + articleUniqueNum],  # applyDoc
                                    result_workNetDictionaty['제출서류양식첨부_' + articleUniqueNum],  # applyDocAttach
                                    result_workNetDictionaty['외국어능력_' + articleUniqueNum],  # bilingual
                                    result_workNetDictionaty['전공_' + articleUniqueNum],  # collgMajor
                                    result_workNetDictionaty['자격면허_' + articleUniqueNum],  # license
                                    result_workNetDictionaty['컴퓨터활용능력_' + articleUniqueNum],  # comCap
                                    result_workNetDictionaty['우대조건_' + articleUniqueNum],  # prfrFactor_detl
                                    result_workNetDictionaty['병역특례채용희망_' + articleUniqueNum],  # wichHireMil
                                    result_workNetDictionaty['장애인채용희망_' + articleUniqueNum],  # wishHireDisabled
                                    result_workNetDictionaty['기타우대사항_' + articleUniqueNum],  # etcPrefer
                                    result_workNetDictionaty['복리후생_' + articleUniqueNum],  # welfare
                                    result_workNetDictionaty['장애인편의시설_' + articleUniqueNum],  # facltDisabled
                                    result_workNetDictionaty['더추가할구인조건_' + articleUniqueNum],  # moreHireCond
                                    result_workNetDictionaty['부서-담당자_' + articleUniqueNum],  # recruitMngr
                                    result_workNetDictionaty['전화번호_' + articleUniqueNum],  # recruitMngrTel1
                                    result_workNetDictionaty['휴대전화_' + articleUniqueNum],  # recruitMngrTel2
                                    result_workNetDictionaty['팩스번호_' + articleUniqueNum],  # faxNo
                                    result_workNetDictionaty['E-mail_' + articleUniqueNum]  # recruitMngrEmail
                                )

                                insertCnt = insertCnt + 1
                                print('DB INSERT COUNT : ', insertCnt)
                                logger.debug('DB INSERT COUNT : {}'.format(insertCnt) )

                                print('DB insert result : ', insertResult)
                                logger.debug('DB insert result : {}'.format(insertResult) )

                        #Scroll Test Fail
                        else:
                            print('정상적으로 스크롤을 진행할 수 있는 화면이 아닙니다. 아마도, 마감된 채용 정보일 것입니다.다음 정보로 넘어갑니다.')
                            #다음 loop로 넘어간다.

                            alertObj = driver.switch_to_alert()
                            alertObj.accept()
                            continue



                except Exception as e_url:
                    print('234:', e_url)

                    continue

        except Exception as e_magam:
            print('@@@마감된 채용 정보입니다.', e_magam)
            logger.error('마감된 채용 정보입니다 : {} '.format(e_magam))

            alertObj = driver.switch_to_alert()
            alertObj.accept()

            continue

    print('###Final_Data : ', result_workNetDictionaty)
    return result_workNetDictionaty

#No.2#########################################################################################################
def bringContentBasicData(driver, searchURL):

    driver.get(searchURL)
    crawledResults = getPagination(driver, searchURL)

    print('최종 크롤링 결과 :', crawledResults)

    return crawledResults


#No.1#########################################################################################################
def worknet_login():

    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")

    prefs = {}
    prefs['profile.default_content_setting_values.notifications'] = 2
    chrome_options.add_experimental_option('prefs', prefs)
    driver_chrome = "C:\\dev_tenspace\\PycharmProjects\\aster_dev_201808\\chromedriver.exe"

    driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=driver_chrome)
    visitedURL = "http://www.work.go.kr/seekWantedMain.do"

    driver.get(visitedURL)
    userid = 'microscope83'
    userpw = 'Gkstkddbs1!'

    if driver.find_element_by_id('chkKeyboard').is_selected():
        driver.execute_script("arguments[0].click();", driver.find_element_by_id('chkKeyboard'))

        driver.find_element_by_id('custId').send_keys(userid)
        driver.find_element_by_id('pwd').send_keys(userpw)

        driver.find_element_by_id('btnLogin').click()
        print(driver.current_url)

        searchURL = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"
        bringContentBasicData(driver, searchURL)

    else:
        print('키보드 보안 프로그램으로 인해 해결 불가')
        searchURL = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"
        bringContentBasicData(driver, searchURL)

        driver.close()

#if __name__ == "__main__":
#worknetPrj = worknetCrawlerBot()
#worknetPrj.worknet_login()
worknet_login()
