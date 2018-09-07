import logging.config
import logging.handlers
import logging.handlers
import os
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from aster_dev_201808.aster879.worknet_just import mysqlConnection_just as mySQL_conn

os.environ['MOS_HEADLESS'] = "1"


class worknetCrawlerBot():

















    def __init__(self):
        print('start')
        #
        # self.binary = FirefoxBinary("/usr/bin/firefox", log_file=sys.stdout)
        # self.hereWork = "worknet_crawling"
        #
        # self.currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
        #     time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)
        #
        # self.logger = logging.getLogger(self.hereWork + '_logging')

        self.hereWork = "worknet_crawling"

        self.currTime = str(time.localtime().tm_year) + '_' + str(time.localtime().tm_mon) + '_' + str(
            time.localtime().tm_mday) + '_' + str(time.localtime().tm_hour)

        self.logger = logging.getLogger(self.hereWork + '_logging')
        self.logger.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        self.file_max_bytes = 10 * 1024 * 1024  # log file size : 10MB
        self.fileHandler = logging.handlers.RotatingFileHandler(
            'C:\\dev_tenspace\\PycharmProjects\\log\\' + self.hereWork + '_crawlerbot_logging_' + self.currTime,
            maxBytes=self.file_max_bytes, encoding='UTF-8', backupCount=10)
        self.streamHandler = logging.StreamHandler()

        self.fileHandler.setFormatter(self.formatter)
        self.streamHandler.setFormatter(self.formatter)

        self.logger.addHandler(self.fileHandler)

        self.start_time_all = time.time()
    #
    # def getCorpDetailInfo(self, driver, current_url, articleUniqueNumber, result_workNetDict):
    #
    #     print('getCorpDetailInfo:', current_url)
    #     corpJobDetailArticle = self.autoScroller(driver)
    #
    #     #기본정보(table)
    #     trCntHTML = corpJobDetailArticle.select(
    #         'div#content-area > div > div:nth-of-type(2) > table > tbody > tr')
    #
    #     result_workNetDict['회사명_기업정보' + articleUniqueNumber] = ''
    #     result_workNetDict['회사주소_기업정보' + articleUniqueNumber] = ''
    #     result_workNetDict['기업형태_기업정보' + articleUniqueNumber] = ''
    #     result_workNetDict['자본금_기업정보' + articleUniqueNumber] = ''
    #     result_workNetDict['업종_기업정보' + articleUniqueNumber] = ''
    #     result_workNetDict['주요제품명_기업정보' + articleUniqueNumber] = ''
    #
    #
    #     for trlength in range(len(trCntHTML)):
    #         thCntHTML = corpJobDetailArticle.select(
    #             'div#content-area > div > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
    #                 trlength + 1) +') > th')
    #
    #         if len(thCntHTML) == 1:
    #             print('회사명 혹은 회사 주소 부분임')
    #             thName = corpJobDetailArticle.select(
    #                 'div#content-area > div > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
    #                     trlength + 1) + ') > th')[0].text
    #
    #             tdName = corpJobDetailArticle.select(
    #                 'div#content-area > div > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
    #                     trlength + 1) + ') > td:nth-of-type(1)')[0].text
    #
    #             print(thName, ':', tdName)
    #             result_workNetDict[thName+'_'+articleUniqueNumber] = tdName
    #
    #
    #         else:
    #             print('기업형태, 자본금, 업종, 주요제품명 부분임')
    #             for thlength in range(len(thCntHTML)):
    #                 thName = corpJobDetailArticle.select(
    #                     'div#content-area > div > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
    #                         trlength + 1) + ') > th:nth-of-type(' + str(
    #                         thlength + 1) + ')')[0].text
    #                 tdName = corpJobDetailArticle.select(
    #                     'div#content-area > div > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
    #                         trlength + 1) + ') > td:nth-of-type(' + str(
    #                         thlength + 1) + ')')[0].text
    #
    #                 print(thName, ':', tdName)
    #                 result_workNetDict[thName+'_'+articleUniqueNumber] = tdName


    def getAllGongoInfo(self, corpJobDetailArticle, result_workNetDictionaty, articleUniqueNum):

        doneOrNot = False

        corpinfolist01 = []
        corpinfolist01contents = []
        corpinfolist01contents2 = []
        corpinfolist02 = []
        corpinfolist02contents = []
        corpJobDetailArticle2 = corpJobDetailArticle

        # Maria-Field : 조회수 : searchArticleCnt
        searchArticleCntTitle = corpJobDetailArticle2.select(
            'div#content-area > div > div:nth-of-type(3) > p > b:nth-of-type(1)')[
            0].text.replace(
            "  ", "").replace(" ", "").replace("    ", "").replace("        ", "").replace(
            "\n", "").replace("\xa0", "").replace("\t", "").replace(",", "&")



        # Maria-Data : 조회수 '숫자'
        searchArticleCnt = \
            corpJobDetailArticle2.select('div#content-area > div > div:nth-of-type(3) > p')[
                0].text.replace(
                "  ", "").replace(" ", "").replace("    ", "").replace("        ", "").replace(
                "\n", "").replace("\xa0", "").split("|")[0].split(searchArticleCntTitle)[
                1].split("명")[0]

        print(searchArticleCntTitle, ':', searchArticleCnt) # 조회수:숫자

        # DATA : searchArticleCnt
        result_workNetDictionaty[
            searchArticleCntTitle + '_' + articleUniqueNum] = searchArticleCnt
        # 조회수_구인인증번:숫자

        # Maria-Field : '지원자' : articleApplyCnt
        applicantArticleCntTitle = corpJobDetailArticle2.select(
            'div#content-area > div > div:nth-of-type(3) > p > b:nth-of-type(2)')[
            0].text.replace(
            "  ", "").replace(" ", "").replace("    ", "").replace("        ", "").replace(
            "\n", "").replace("\xa0", "").replace("\t", "").replace(",", "&")



        # Maria-Data : 지원자 '숫자'
        applicantArticleCnt = \
            corpJobDetailArticle2.select('div#content-area > div > div:nth-of-type(3) > p')[
                0].text.replace(
                "  ", "").replace(" ", "").replace("    ", "").replace("        ", "").replace(
                "\n", "").replace("\xa0", "").split("|")[1].split(applicantArticleCntTitle)[
                1].split("명")[0]

        # DATA : articleApplyCnt
        result_workNetDictionaty[
            applicantArticleCntTitle + '_' + articleUniqueNum] = applicantArticleCnt

        print(applicantArticleCntTitle, ":", applicantArticleCnt) #지원자:숫자

        self.logger.debug('{}:{}명, {}:{}명'.format(searchArticleCntTitle, int(searchArticleCnt),
                                                  applicantArticleCntTitle,
                                                  int(applicantArticleCnt)))

        # 회사 상세 정보
        # 회사 로고 img directory
        # Maria-Field : 회사 이미지 사용 유무 : corpImageYN(boolean)
        corpImgDir = corpJobDetailArticle2.find(id='logoImg')['src']
        if 'none_imglogo.gif' in corpImgDir:
            self.logger.debug('회사 이미지 사용하지 않음')
            print('회사 이미지 사용하지 않음')
            result_workNetDictionaty['corpImgDir_' + articleUniqueNum] = ''
        else:
            # Maria-Data : corpImgDir
            self.logger.debug('회사 이미지 저장 디렉토리 : {}'.format(corpImgDir))
            print('회사 이미지 사용')
            result_workNetDictionaty['corpImgDir_' + articleUniqueNum] = corpImgDir

        # 회사 소개 상세 정보(회사명, 대표자명, 근로자수, 자본금, 연매출액, 업종, 주요사업내용, 회사주소, 홈페이지)
        detailCorpInfo_length = len(corpJobDetailArticle2.select('div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr'))

        print('회사 소개 정보 길이:', detailCorpInfo_length)

        result_workNetDictionaty['기업평가글_' + articleUniqueNum] = ''

        # 회사 소개 항목을 덜 채운 상태임.
        if detailCorpInfo_length != 0:

            # 회사 소개 항목을 모두 채운 상태임.
            # detailCorpInfo_length 자체가 len()의 결과물이기 때문에 다시 len()으로 감싸놓을 필요 없음.

            for tr_length in range(detailCorpInfo_length):
                trUnderThLen = len(corpJobDetailArticle2.select(
                    'div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                        tr_length + 1) + ') > th'))

                detailPartContent = ''
                detailPartContent2 = ''

                for thORtd_length in range(trUnderThLen):
                    # Maria-Filed :
                    # 회사명: corpNm_detl/대표자명: ceoNm/근로자수: workerCnt/ 자본금: jabon/
                    # 연매출액: yearIncome/업종: jobKind/주요사업내용: jobKind_main/회사주소:corpAddr
                    # 홈페이지: homepage
                    detailPartTitle = corpJobDetailArticle2.select(
                        'div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                            tr_length + 1) + ') > th:nth-of-type(' + str(
                            thORtd_length + 1) + ')')[0].text.replace(
                                " ", "").replace(
                                "  ", " ").replace(
                                "	", " ").replace(
                                "    ", " ").replace(
                                "    ", " ").replace(
                                "     ", " ").replace(
                                "      ", " ").replace(
                                "       ", " ").replace(
                                "        ", " ").replace(
                                "          ", " ").replace(
                                "\n", " ").replace(
                                "\xa0", "").replace(
                                "\t", "").replace(
                                ",", "&")

                    print('detailPartTitle:', detailPartTitle)

                    detailPartContent = corpJobDetailArticle2.select(
                        'div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                            tr_length + 1) + ') > td:nth-of-type(' + str(
                            thORtd_length + 1) + ')')[0].text.replace(
                                #" ", " ").replace(
                                "  ", " ").replace(
                                "	", " ").replace(
                                "    ", " ").replace(
                                "    ", " ").replace(
                                "     ", " ").replace(
                                "      ", " ").replace(
                                "       ", " ").replace(
                                "        ", " ").replace(
                                "          ", " ").replace(
                                "\n", " ").replace(
                                "\xa0", "").replace(
                                "\t", "").replace(
                                ",", "&")

                    print('detailPartContent:', detailPartContent)

                    # DATA : corpNm_detail ~ homepage
                    corpinfolist01.append(detailPartTitle)
                    corpinfolist01contents.append(detailPartContent)
                    
                    #기업소개상단테이블의 회사명 하단에 추가 기업 설명부분 추출
                    try:
                        print('기업소개상단테이블의 회사명 하단에 추가 기업 설명부분 추출 존재')
                        detailTextExpLen = len(corpJobDetailArticle2.select(
                            'div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                                tr_length + 1) + ') > td:nth-of-type(' + str(
                                thORtd_length + 1) + ') > dl > dd > ul > li'))

                        for jenRealbad in range(detailTextExpLen):
                            print('!@#!@#1111')
                            detailPartContent2 = corpJobDetailArticle2.select(
                                'div#content-area > div > div:nth-of-type(4) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                                    tr_length + 1) + ') > td:nth-of-type(' + str(
                                    thORtd_length + 1) + ') > dl > dd > ul > li:nth-of-type(' + str(jenRealbad + 1) + ') > span > a')[0].text.replace(
                                        "  ", " ").replace(
                                        "	", " ").replace(
                                        "    ", " ").replace(
                                        "    ", " ").replace(
                                        "     ", " ").replace(
                                        "      ", " ").replace(
                                        "       ", " ").replace(
                                        "        ", " ").replace(
                                        "          ", " ").replace(
                                        "\n", " ").replace(
                                        "\xa0", "").replace(
                                        "\t", "").replace(
                                        "0,0", "").replace(
                                        ", ", "")

                            corpinfolist01contents2.append(detailPartContent2)

                            print('!@#!@#2222')
                            result_workNetDictionaty['기업평가글_' + articleUniqueNum] = str(corpinfolist01contents2).replace(",", "+")

                            print('기업 평가글 :', result_workNetDictionaty['기업평가글_' + articleUniqueNum])
                            
                    except Exception as e:
                        print('기업소개상단테이블의 회사명 하단에 추가 기업 설명부분 존재하지 않음.')
                        print('기업 명 하단의 기업 평가 Text가 존재하지 않습니다.', e)


            print('corpinfolist01:', corpinfolist01)
            for listleng in range(len(corpinfolist01)):
                print('corpinfolist01', corpinfolist01[listleng] + '_' + articleUniqueNum)
                print('@@@', corpinfolist01[listleng] + '_' + articleUniqueNum, '=', corpinfolist01contents[listleng])

                result_workNetDictionaty[corpinfolist01[listleng] + '_' + articleUniqueNum] = corpinfolist01contents[listleng]

                #result_workNetDictionaty[corpinfolist01[listleng] + '_' + articleUniqueNum] = detailPartContent
            self.logger.debug('{}-{}.{}:{}'.format(tr_length, thORtd_length, detailPartTitle,detailPartContent))
            print('204_line_result_workNetDictionaty_01 :', result_workNetDictionaty)

        else:
            print('HTML 구조가 변경됨')
            # print('detailCorpInfo_length가 7이 아닙니다.')
            if detailCorpInfo_length == 0:
                # 회사 소개 항목을 모두 채운 상태임.
                # detailCorpInfo_length 자체가 len()의 결과물이기 때문에 다시 len()으로 감싸놓을 필요 없음.

                for tr_length in range(detailCorpInfo_length):
                    trUnderThLen = len(corpJobDetailArticle2.select(
                        'div#content-area > div > div:nth-of-type(5) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                            tr_length + 1) + ') > th'))

                    for thORtd_length in range(trUnderThLen):
                        # Maria-Filed :
                        # 회사명: corpNm_detl/대표자명: ceoNm/근로자수: workerCnt/ 자본금: jabon/
                        # 연매출액: yearIncome/업종: jobKind/주요사업내용: jobKind_main/회사주소:corpAddr
                        # 홈페이지: homepage
                        detailPartTitle = corpJobDetailArticle2.select(
                            'div#content-area > div > div:nth-of-type(5) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                                tr_length + 1) + ') > th:nth-of-type(' + str(
                                thORtd_length + 1) + ')')[0].text.replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            "0,0", "").replace(
                            ", ", "")

                        print('detailPartTitle:', detailPartTitle)

                        detailPartContent = corpJobDetailArticle2.select(
                            'div#content-area > div > div:nth-of-type(5) > div:nth-of-type(2) > table > tbody > tr:nth-of-type(' + str(
                                tr_length + 1) + ') > td:nth-of-type(' + str(
                                thORtd_length + 1) + ')')[0].text.replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            "0,0", "").replace(
                            ", ", "")

                        print('detailPartContent:', detailPartContent)

                        # DATA : corpNm_detail ~ homepage

                        corpinfolist01.append(detailPartTitle)
                        corpinfolist01contents.append(detailPartContent)

                print('corpinfolist01_02:', corpinfolist01)

                for listleng in range(len(corpinfolist01)):
                    print('corpinfolist01_02:', corpinfolist01[listleng] + '_' + articleUniqueNum)
                    print(corpinfolist01[listleng] + '_' + articleUniqueNum, '=', corpinfolist01contents[listleng])

                    result_workNetDictionaty[corpinfolist01[listleng] + '_' + articleUniqueNum] = corpinfolist01contents[listleng]

                self.logger.debug('{}-{}.{}:{}'.format(tr_length, thORtd_length, detailPartTitle, detailPartContent))
                print('204_line_result_workNetDictionaty_02:', result_workNetDictionaty)

            else:
                self.logger.debug('회사 소개가 없습니다.')
                print('회사 소개가 없음')

                self.logger.debug('회사 소개 tr 갯수 : {}'.format(detailCorpInfo_length))
                print('회사 소개 tr테그 개수: ', detailCorpInfo_length)

                #변수 생성
                #회사명, 대표자명, 근로자수, 자본금, 연매출액, 업종, 주요사업내용, 회사주소, 홈페이지
                # result_workNetDictionaty['회사명_' + articleUniqueNum] = ''
                # result_workNetDictionaty['대표자명_' + articleUniqueNum] = ''
                # result_workNetDictionaty['근로자수_' + articleUniqueNum] = ''
                # result_workNetDictionaty['자본금_' + articleUniqueNum] = ''
                # result_workNetDictionaty['연매출액_' + articleUniqueNum] = ''
                # result_workNetDictionaty['업종_' + articleUniqueNum] = ''
                # result_workNetDictionaty['주요사업내용_' + articleUniqueNum] = ''
                # result_workNetDictionaty['회사주소_' + articleUniqueNum] = ''
                # result_workNetDictionaty['홈페이지_' + articleUniqueNum] = ''

        # Maria-Field :
        # 회사 공고 지원자 숙지 사항(지원자격, 근무조건, 고용형태)
        alertApplicant_len = len(corpJobDetailArticle2.select(
            'div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li'))
        # print('@', alertApplicant_len)
        for alert_length in range(alertApplicant_len):
            alertNoticeTitle = corpJobDetailArticle2.select(
                'div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                    alert_length + 1) + ') > strong')[0].text.replace(
                "  ", " ").replace(
                "	", " ").replace(
                "    ", " ").replace(
                "    ", " ").replace(
                "     ", " ").replace(
                "      ", " ").replace(
                "       ", " ").replace(
                "        ", " ").replace(
                "          ", " ").replace(
                "\n", " ").replace(
                "\xa0", "").replace(
                "\t", "").replace(
                "0,0", "").replace(
                ", ", "")

            # 지원자격, 근무조건, 고용형태(타이틀)
            self.logger.debug('#{}'.format(alertNoticeTitle))
            print(alertNoticeTitle)
            alertNoticecontent_len = len(corpJobDetailArticle2.select(
                'div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                    alert_length + 1) + ') > dl > dt'))

            if alertNoticecontent_len != 0:
                for alterNotice_length in range(alertNoticecontent_len):
                    # 지원자격: applyRequire/근무조건: workCondition/고용형태: hireType 각각의 세부항목
                    articleNoticeDetailTitle = corpJobDetailArticle2.select(
                        'div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                            alert_length + 1) + ') > dl > dt:nth-of-type(' + str(
                            alterNotice_length + 1) + ')')[0].text.replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            "0,0", "").replace(
                            ", ", "")

                    articleNoticeDetailContent = corpJobDetailArticle2.select(
                        'div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(1) > ul > li:nth-of-type(' + str(
                            alert_length + 1) + ') > dl > dd:nth-of-type(' + str(
                            alterNotice_length + 1) + ')')[0].text.replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            "0,0", "").replace(
                            ", ", "")

                    # DATA : applyRequire ~ hireType
                    result_workNetDictionaty[articleNoticeDetailTitle + '_' + articleUniqueNum] = articleNoticeDetailContent
                    print(articleNoticeDetailTitle, ":", articleNoticeDetailContent)

                else:
                    print('기초 정보 즉, 지원자격, 근무조건, 고용형태 에 대한 정보가 등록되어 있지 않습니다.')
                    result_workNetDictionaty['경력_' + articleUniqueNum] = ''
                    result_workNetDictionaty['학력_' + articleUniqueNum] = ''
                    result_workNetDictionaty['근무지역_' + articleUniqueNum] = ''
                    result_workNetDictionaty['임금_' + articleUniqueNum] = ''
                    result_workNetDictionaty['고용형태_' + articleUniqueNum] = ''
                    result_workNetDictionaty['근무형태_' + articleUniqueNum] = ''


        # 복리후생
        # welfare_len = len(corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(2) span > img'))
        # corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(4) > div#intereView > div:nth-of-type(2) span > img:nth-of-type(' +  + ')')
        # 복리후생 조건을 img 테그의 alt 값으로 설정하여 다른 이미지 지정하는 방식임. 특별한 키값이 존재하는 것이 아니라서 감지하기 어려움.

        # 기업 홍보 존
        # corpJobDetailArticle.select('div#corpInfoView > div#extCoinfo > iframe#corpInfo > ')
        # iframe을 잡아야 함.

        # Maria-Field : 모집요강제목: mojibYoGangTitle/ 구인인증번호: mojibYoGangSerialNo
        mojibYoGangTitle = corpJobDetailArticle2.select('div.empdetail > h4')[
            0].text.replace(
            "  ", "").replace(" ", "").replace("    ", "").replace("        ", "").replace(
            "\n", "").replace("\xa0", "")
        mojibYoGangSerialNo = corpJobDetailArticle2.select('div.empdetail > font')[
            0].text.replace(
            "  ", "").replace(" ", "").replace("    ", "").replace("        ", "").replace(
            "\n", "").replace("\xa0", "")

        # 기업 홍보존 하단의 6개 테이블 출력 부분 : 모집요강, 근무조건, 전형방법, 우대사항, 기타사항, 채용담당자

        # 모집요강 구인인증번호 출력
        self.logger.debug('{} {}'.format(mojibYoGangTitle, mojibYoGangSerialNo))
        lengthOfTable = len(corpJobDetailArticle2.select('div.empdetail > table.info_list'))
        print('모집 요강 구인 인증 번호: ', mojibYoGangSerialNo)
        self.logger.debug('$$: {}'.format(lengthOfTable))
        #print('$$', lengthOfTable)

        for infoTable_length in range(lengthOfTable):
            print()
            self.logger.debug('infoTable_No{}'.format(str(infoTable_length + 1)))
            print('정보 테이블 번호 : ', str(infoTable_length + 1) )

            # Maria-Field :
            infoTableTitle = corpJobDetailArticle2.select(
                'div.empdetail > table:nth-of-type(' + str(
                    infoTable_length + 1) + ') > caption')[0].text.replace(
                " ", "").replace(
                "  ", " ").replace(
                "	", " ").replace(
                "    ", " ").replace(
                "    ", " ").replace(
                "     ", " ").replace(
                "      ", " ").replace(
                "       ", " ").replace(
                "        ", " ").replace(
                "          ", " ").replace(
                "\n"," ").replace(
                "\xa0", "").replace(
                "\t", "").replace(
                ",", "&")

            self.logger.debug('-{}'.format(corpJobDetailArticle2.select(
                'div.empdetail > table:nth-of-type(' + str(
                    infoTable_length + 1) + ') > caption')[0].text.replace(
                " ", "").replace(
                "  ", " ").replace(
                "	", " ").replace(
                "    ", " ").replace(
                "    ", " ").replace(
                "     ", " ").replace(
                "      ", " ").replace(
                "       ", " ").replace(
                "        ", " ").replace(
                "          ", " ").replace(
                "\n"," ").replace(
                "\xa0", "").replace(
                "\t", "").replace(
                ",", "&")
            ))

            length_table_content = len(corpJobDetailArticle2.select(
                'div.empdetail > table:nth-of-type(' + str(
                    infoTable_length + 1) + ') > tbody > tr'))
            # nth-of-type()를 적용시키기 위해서는 class 명을 명시하지 말고 nth-of-type을 적용하여야 한다.

            print()
            self.logger.debug('{} : {}'.format(infoTableTitle, length_table_content))

            if length_table_content == 1:
                try:
                    infoTableContent_title = corpJobDetailArticle2.select(
                        'div.empdetail > table:nth-of-type(' + str(
                            infoTable_length + 1) + ') > thead > tr > th')[0].text.replace(
                        " ", "").replace(
                        "  ", " ").replace(
                        "	", " ").replace(
                        "    ", " ").replace(
                        "    ", " ").replace(
                        "     ", " ").replace(
                        "      ", " ").replace(
                        "       ", " ").replace(
                        "        ", " ").replace(
                        "          ", " ").replace(
                        "\n", " ").replace(
                        "\xa0", "").replace(
                        "\t", "").replace(
                        ",", "&")

                    infoTableContent_contents = corpJobDetailArticle2.select(
                        'div.empdetail > table:nth-of-type(' + str(
                            infoTable_length + 1) + ') > tbody > tr > td')[0].text.replace(
                        #" ", " ").replace(
                        "  ", " ").replace(
                        "	", " ").replace(
                        "    ", " ").replace(
                        "    ", " ").replace(
                        "     ", " ").replace(
                        "      ", " ").replace(
                        "       ", " ").replace(
                        "        ", " ").replace(
                        "          ", " ").replace(
                        "\n", " ").replace(
                        "\xa0", "").replace(
                        "\t", "").replace(
                        ",", "&")

                    result_workNetDictionaty[
                        infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                    print(infoTableContent_title,":", articleUniqueNum)


                    self.logger.debug('{}'.format(result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]))

                except Exception as e_etc:
                    print('이런 경우는 없어야 함. ', e_etc)
                    infoTableContent_title = '더추가할구인조건'
                    infoTableContent_contents = corpJobDetailArticle2.select(
                        'div.empdetail > table:nth-of-type(' + str(
                            infoTable_length + 1) + ') > tbody > tr > td')[0].text.replace(
                        #" ", " ").replace(
                        "  ", " ").replace(
                        "	", " ").replace(
                        "    ", " ").replace(
                        "    ", " ").replace(
                        "     ", " ").replace(
                        "      ", " ").replace(
                        "       ", " ").replace(
                        "        ", " ").replace(
                        "          ", " ").replace(
                        "\n", " ").replace(
                        "\xa0", "").replace(
                        "\t", "").replace(
                        ",", "&")

                    result_workNetDictionaty[
                        infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                    self.logger.debug('{}'.format(result_workNetDictionaty[
                                                      infoTableContent_title + '_' + articleUniqueNum]))

                # 평균연봉
                try:
                    # //*[@id="content-area"]/div/div[7]/div[12]/ul/li[3]/strong
                    avgYearWage = corpJobDetailArticle2.select('div.job_planet > ul > li:nth-of-type(3) > strong')[0].text
                    print('평균연봉:', avgYearWage)
                    result_workNetDictionaty['평균연봉_' + articleUniqueNum] = avgYearWage

                except Exception as e:
                    print('평균연봉에 대한 정보가 없습니다.')
                    result_workNetDictionaty['평균연봉_' + articleUniqueNum] = ''

            elif length_table_content == 3:
                print('회사 주소 및 지도 표시')

                for infoTable_content_length in range(length_table_content - 1):
                    self.logger.debug('infoTable_content_No.{}'.format(str(infoTable_content_length + 1)))
                    print( '회사 주소 및 지도 표시 영역 정보 테이블 번호 : ', str(infoTable_content_length + 1) )

                    # Maria-Field :
                    try:
                        infoTableContent_title = corpJobDetailArticle2.select(
                            'div.empdetail > table:nth-of-type(' + str(
                                infoTable_length + 1) + ') > thead > tr > th')[
                            0].text.replace(
                            " ", "").replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            ",", "&")

                        infoTableContent_contents = corpJobDetailArticle2.select(
                            'div.empdetail > table:nth-of-type(' + str(
                                infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                infoTable_content_length + 1) + ') > td')[0].text.replace(
                            #" ", " ").replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            ",", "&")

                        result_workNetDictionaty[
                            infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents

                        print(infoTableContent_title, ":", infoTableContent_contents)

                        self.logger.debug('{}'.format(result_workNetDictionaty[
                                                          infoTableContent_title + '_' + articleUniqueNum]))

                    except Exception as e_etc:
                        print('thead 태그가 없는 경우가 대부분임_정상인 상황 : ', e_etc)
                        infoTableContent_contents = corpJobDetailArticle2.select(
                            'div.empdetail > table:nth-of-type(' + str(
                                infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                infoTable_content_length + 1) + ') > td')[0].text.replace(
                            #" ", " ").replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            ",", "&")

                        result_workNetDictionaty[
                            infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents

                        print('thead가 없는 경우: ', infoTableContent_contents)

                        self.logger.debug('{}'.format(result_workNetDictionaty[
                                                          infoTableContent_title + '_' + articleUniqueNum]))
                # 평균연봉
                try:
                    # //*[@id="content-area"]/div/div[7]/div[12]/ul/li[3]/strong
                    avgYearWage = corpJobDetailArticle2.select('div.job_planet > ul > li:nth-of-type(3) > strong')[0].text

                    print('평균연봉:', avgYearWage)
                    result_workNetDictionaty['평균연봉_' + articleUniqueNum] = avgYearWage

                except Exception as e:
                    print('평균연봉에 대한 정보가 없습니다.')
                    result_workNetDictionaty['평균연봉_' + articleUniqueNum] = ''

            else:
                for infoTable_content_length in range(length_table_content):
                    #print('테이블 내용이 1개가 아닌 경우의 정보 테이블 번호 : ', str(infoTable_content_length + 1))

                    # Maria-Field :
                    try:
                        infoTableContent_title = corpJobDetailArticle2.select(
                            'div.empdetail > table:nth-of-type(' + str(
                                infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                infoTable_content_length + 1) + ') > th')[0].text.replace(
                            " ", "").replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            ",", "&")

                        infoTableContent_contents = corpJobDetailArticle2.select(
                            'div.empdetail > table:nth-of-type(' + str(
                                infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                infoTable_content_length + 1) + ') > td')[0].text.replace(
                            #" ", " ").replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            ",", "&")


                        result_workNetDictionaty[
                            infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents
                        self.logger.debug('{}'.format(result_workNetDictionaty[
                                                          infoTableContent_title + '_' + articleUniqueNum]))

                    except Exception as e_th:
                        print('기타사항 -  테이블 진입 : th 태그가 없음', e_th)

                        infoTableContent_title = '더추가할구인조건'

                        infoTableContent_contents = corpJobDetailArticle2.select(
                            'div.empdetail > table:nth-of-type(' + str(
                                infoTable_length + 1) + ') > tbody > tr:nth-of-type(' + str(
                                infoTable_content_length + 1) + ') > td')[0].text.replace(
                            #" ", " ").replace(
                            "  ", " ").replace(
                            "	", " ").replace(
                            "    ", " ").replace(
                            "    ", " ").replace(
                            "     ", " ").replace(
                            "      ", " ").replace(
                            "       ", " ").replace(
                            "        ", " ").replace(
                            "          ", " ").replace(
                            "\n", " ").replace(
                            "\xa0", "").replace(
                            "\t", "").replace(
                            ",", "&")


                        result_workNetDictionaty[
                            infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents

                        print('기타사항', infoTableContent_title, ":", infoTableContent_contents)

                        self.logger.debug('{}'.format(result_workNetDictionaty[
                                                          infoTableContent_title + '_' + articleUniqueNum]))

                # Maria-Field :
                # 모집요강= 모집직종:recruitJobKind / 직종키워드:jobKindKeyword / 관련직종:relatedJobKind / 직무내용:whatWork
                #          경력조건:experOpt / 학력:eduCond / 고용형태:hireType_detl / 모집인원:hireCnt / 근무예정지:workPlace/ 소속산업단지:industCommnt / 인근전철역:nearSubway
                # 근무환경및복리후생: 임금조건: wageCond/ 식사(비)제공: mealOffer/ 근무시간: workTime/ 근무형태: jobType/ 사회보험: Socialensure/ 퇴직금지급방법: retirePay
                # 전형방법: 접수마감일: applyDueDate/ 전형방법: howToRecruit_detl/ 접수방법: howToApply_detl/ 제출서류준비물: applyDoc/ 제출서류양식 첨부: appliDocAttach
                # 우대사항: 외국어능력: bilingual/ 전공: collgMajor/ 자격면허: license/ 컴퓨터활용능력: comCap/ 우대조건: prfrFactor_detl
                #          병역특례채용희망: wishHireMil/ 장애인채용희망: wishHireDisabled/ 기타우대사항: etcPrefer/ 복리후생: welfare/ 장애인편의시설: facltDisabled
                # 기타입력사항: 더추가할구인조건: moreHireCond

                # 평균연봉
                try:
                    # //*[@id="content-area"]/div/div[7]/div[12]/ul/li[3]/strong
                    avgYearWage = corpJobDetailArticle2.select('div.job_planet > ul > li:nth-of-type(3) > strong')[0].text
                    print('평균연봉:', avgYearWage)
                    result_workNetDictionaty['평균연봉_' + articleUniqueNum] = avgYearWage



                except Exception as e:
                    print('평균연봉에 대한 정보가 없습니다.')
                    result_workNetDictionaty['평균연봉_' + articleUniqueNum] = ''


                # DATA : recruitFactors, workEnv_welfare, howtoapply, preferFactor, etc
                result_workNetDictionaty[
                    infoTableContent_title + '_' + articleUniqueNum] = infoTableContent_contents.replace("\t", "")

                #print('테이블 내용이 1개가 아닌 경우 :', infoTableContent_title, ":", infoTableContent_contents.replace("\t", ""))
                print(infoTableContent_title, ":", infoTableContent_contents.replace("\t", ""))

                self.logger.debug('#{},{}'.format(infoTableContent_title,result_workNetDictionaty[infoTableContent_title + '_' + articleUniqueNum]))
                self.logger.debug('{}:{}'.format(infoTableContent_title, infoTableContent_contents))
                # End of Loop



        # 채용담당자
        try:
            #단순히 '채용담당자'라는 단어가 존재하는 지 확인하기 위함.
            recruitManagerTitle = corpJobDetailArticle2.select(
                'div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > caption')[
                0].text.replace(
                " ", "").replace(
                "  ", " ").replace(
                "	", " ").replace(
                "    ", " ").replace(
                "    ", " ").replace(
                "     ", " ").replace(
                "      ", " ").replace(
                "       ", " ").replace(
                "        ", " ").replace(
                "          ", " ").replace(
                "\n"," ").replace(
                "\xa0", "").replace(
                "\t", "").replace(
                ",", "&")
        except Exception as e:
            print('채용 담당자 항목 없음.')


        try:
            #클릭 이벤트로 잡혀 있는 커버를 벗긴다.
            # link = self.driver.find_element_by_link_text('채용담당자 정보보기')
            # link.click()

            length_recruitManagerInfo = len(corpJobDetailArticle2.select(
                'div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > tbody > tr'))

            for recruitMngInf_len in range(length_recruitManagerInfo):
                recruitManagerDetailTitle = corpJobDetailArticle2.select(
                    'div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(
                        recruitMngInf_len + 1) + ') > th')[0].text.replace(
                    " ", "").replace(
                    "  ", " ").replace(
                    "	", " ").replace(
                    "    ", " ").replace(
                    "    ", " ").replace(
                    "     ", " ").replace(
                    "      ", " ").replace(
                    "       ", " ").replace(
                    "        ", " ").replace(
                    "          ", " ").replace(
                    "\n", " ").replace(
                    "\xa0", "").replace(
                    "\t", "").replace(
                    ",", "&")

                recruitManagerDetailContents = corpJobDetailArticle2.select(
                    'div.empdetail > div:nth-of-type(5) > div:nth-of-type(1) > table > tbody > tr:nth-of-type(' + str(
                        recruitMngInf_len + 1) + ') > td')[0].text.replace(
                    #"-", " ").replace(
                    #" ", " ").replace(
                    "	", " ").replace(
                    "    ", " ").replace(
                    "    ", " ").replace(
                    "     ", " ").replace(
                    "      ", " ").replace(
                    "       ", " ").replace(
                    "        ", " ").replace(
                    "          ", " ").replace(
                    "                   ", " ").replace(
                    "\n", "").replace(
                    "\xa0", "")

                corpinfolist02.append(recruitManagerDetailTitle)
                corpinfolist02contents.append(recruitManagerDetailContents)
            print('corpinfolist02:', corpinfolist02, 'corpinfolist02contents:', corpinfolist02contents)

            if '전화번호' or '부서/담당자' in corpinfolist02:

                print('부서/담당자 항목이 존재함')

                print('부서/담당자_' + articleUniqueNum)
                print('전화번호_' + articleUniqueNum)

                # DATA : 부서/담당자: recruitMngr / 전화번호: recruitMngrTel1 / 휴대전화: recruitMngrTel2/ 팩스번호: faxNo / email: recruitMngrEmail

                for lengthList in range(len(corpinfolist02)):
                    print(corpinfolist02[lengthList])
                    print(corpinfolist02contents[lengthList])

                    result_workNetDictionaty[corpinfolist02[lengthList]+ '_' + articleUniqueNum] = corpinfolist02contents[lengthList]

                #result_workNetDictionaty[recruitManagerDetailTitle + '_' + articleUniqueNum] = recruitManagerDetailContents
                self.logger.debug('{}:{}'.format(recruitManagerDetailTitle, recruitManagerDetailContents))

                print('743_line_result_workNetDictionaty:', result_workNetDictionaty)

        except Exception as e:
            print('채용 담당자의 상세 정보 없음 ->', e)
            result_workNetDictionaty['전화번호_' + articleUniqueNum] = '-'
            result_workNetDictionaty['부서/담당자_' + articleUniqueNum] = '-'
            result_workNetDictionaty['휴대전화_' + articleUniqueNum] = '-'
            result_workNetDictionaty['팩스번호_' + articleUniqueNum] = '-'
            result_workNetDictionaty['E-mail_' + articleUniqueNum] = '-'

        insertCnt = 0
        self.exeptioonVal = ''
        try:

            print('LOG:', result_workNetDictionaty)
            # Test print
            self.logger.debug('DB INSERT : '
                         '{},{},{},{},{},{},{},{},{},{},'
                         '{},{},{},{},{},{},{},{},{},{},'
                         '{},{},{},{},{},{},{},{},{},{},'
                         '{},{},{},{},{},{},{},{},{},{},'
                         '{},{},{},{},{},{},{},{},{},{},'
                         '{},{},{},{}'.format(
                result_workNetDictionaty['구인인증번호_' + articleUniqueNum],  # articleUniqueNum
                result_workNetDictionaty['회사명_' + articleUniqueNum],  # corpNm
                result_workNetDictionaty['공고제목_' + articleUniqueNum],  # corpWantJob
                #result_workNetDictionaty['공고제목상세_' + articleUniqueNum],  # corpRecruitArticleTitle
                result_workNetDictionaty['조회수_' + articleUniqueNum],  # searchArticleCnt
                result_workNetDictionaty['지원자_' + articleUniqueNum],  # applicantArticleCnt
                result_workNetDictionaty['corpImgDir_' + articleUniqueNum],  # corpImgDir
                result_workNetDictionaty['회사명_' + articleUniqueNum],  # corpNm_detl
                result_workNetDictionaty['대표자명_' + articleUniqueNum],  # ceoNm
                result_workNetDictionaty['근로자수_' + articleUniqueNum],  # workerCnt
                result_workNetDictionaty['자본금_' + articleUniqueNum],  # jabon
                result_workNetDictionaty['연매출액_' + articleUniqueNum],  # yearIncome
                result_workNetDictionaty['업종_' + articleUniqueNum],  # jobKind
                result_workNetDictionaty['주요사업내용_' + articleUniqueNum],  # jobKind_main
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
                #result_workNetDictionaty['식사(비)제공_' + articleUniqueNum],  # mealOffer
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
                result_workNetDictionaty['부서/담당자_' + articleUniqueNum],  # recruitMngr
                result_workNetDictionaty['전화번호_' + articleUniqueNum],  # recruitMngrTel1
                result_workNetDictionaty['휴대전화_' + articleUniqueNum],  # recruitMngrTel2
                result_workNetDictionaty['팩스번호_' + articleUniqueNum],  # faxNo
                result_workNetDictionaty['E-mail_' + articleUniqueNum],  # recruitMngrEmail
                result_workNetDictionaty['기업종별_' + articleUniqueNum],    #corpType
                result_workNetDictionaty['기업제시연봉_' + articleUniqueNum], #corpSuggWage
                result_workNetDictionaty['기업채용공고등록일_' + articleUniqueNum],   #corpRegDate
                result_workNetDictionaty['기업평가글_' + articleUniqueNum],       #corpEvalText
                result_workNetDictionaty['평균연봉_' + articleUniqueNum]    #avgYearWage
            )
            )
        except Exception as e:
            print('test print error:', e)
            self.exeptioonVal= e
            print(self.exeptioonVal)
            
            try:
                result_workNetDictionaty[self.exeptioonVal] = ''
                print(result_workNetDictionaty[self.exeptioonVal])
            except Exception as e:
                print(e)

        # DB INSERT
        # print('DB_column_01: ', result_workNetDictionaty['구인인증번호_' + articleUniqueNum])  # articleUniqueNum
        database_connection = mySQL_conn.DatabaseConnection_jeniel()
        try:
            insertResult = database_connection.insert_new_record(
                result_workNetDictionaty['구인인증번호_' + articleUniqueNum].replace("\t", ""),  # articleUniqueNum
                result_workNetDictionaty['회사명_' + articleUniqueNum].replace("\t", ""),  # corpNm
                result_workNetDictionaty['공고제목_' + articleUniqueNum].replace("\t", ""),  # corpWantJob
                #result_workNetDictionaty['공고제목상세_' + articleUniqueNum].replace("\t", ""), # corpRecruitArticleTitle
                result_workNetDictionaty['조회수_' + articleUniqueNum].replace("\t", ""),  # searchArticleCnt
                result_workNetDictionaty['지원자_' + articleUniqueNum].replace("\t", ""),  # applicantArticleCnt
                result_workNetDictionaty['corpImgDir_' + articleUniqueNum].replace("\t", ""),  # corpImgDir
                result_workNetDictionaty['회사명_' + articleUniqueNum].replace("\t", ""),  # corpNm_detl
                result_workNetDictionaty['대표자명_' + articleUniqueNum].replace("\t", ""),  # ceoNm
                result_workNetDictionaty['근로자수_' + articleUniqueNum].replace("\t", ""),  # workerCnt
                result_workNetDictionaty['자본금_' + articleUniqueNum].replace("\t", ""),  # jabon
                result_workNetDictionaty['연매출액_' + articleUniqueNum].replace("\t", ""),  # yearIncome
                result_workNetDictionaty['업종_' + articleUniqueNum].replace("\t", ""),  # jobKind
                result_workNetDictionaty['주요사업내용_' + articleUniqueNum].replace("\t", ""),  # jobKind_main
                result_workNetDictionaty['회사주소_' + articleUniqueNum].replace("\t", ""),  # corpAddr
                result_workNetDictionaty['홈페이지_' + articleUniqueNum].replace("\t", ""),  # homepage
                result_workNetDictionaty['모집직종_' + articleUniqueNum].replace("\t", ""),  # recruitJobKind
                result_workNetDictionaty['직종키워드_' + articleUniqueNum].replace("\t", ""),  # jobKindKeyword
                result_workNetDictionaty['관련직종_' + articleUniqueNum].replace("\t", ""),  # relatedJobKind
                result_workNetDictionaty['직무내용_' + articleUniqueNum].replace("\t", ""),  # whatWork
                result_workNetDictionaty['경력조건_' + articleUniqueNum].replace("\t", ""),  # experOpt
                result_workNetDictionaty['학력_' + articleUniqueNum].replace("\t", ""),  # eduCond
                result_workNetDictionaty['근무지역_' + articleUniqueNum].replace("\t", ""),  # workArea
                result_workNetDictionaty['임금_' + articleUniqueNum].replace("\t", ""),  # wageCond
                result_workNetDictionaty['고용형태_' + articleUniqueNum].replace("\t", ""),  # hireType_detl
                result_workNetDictionaty['모집인원_' + articleUniqueNum].replace("\t", ""),  # hireCnt
                result_workNetDictionaty['근무예정지_' + articleUniqueNum].replace("\t", ""),  # workPlace
                result_workNetDictionaty['소속산업단지_' + articleUniqueNum].replace("\t", ""),  # industCommnt
                result_workNetDictionaty['인근전철역_' + articleUniqueNum].replace("\t", ""),  # nearSubway
                result_workNetDictionaty['임금조건_' + articleUniqueNum].replace("\t", "").replace("&", ""),  # wageCond_detl
                result_workNetDictionaty['식사(비)제공_' + articleUniqueNum].replace("\t", ""),  # mealOffer
                result_workNetDictionaty['근무시간_' + articleUniqueNum].replace("\t", ""),  # workTime
                result_workNetDictionaty['근무형태_' + articleUniqueNum].replace("\t", ""),  # jobType
                result_workNetDictionaty['사회보험_' + articleUniqueNum].replace("\t", ""),  # socialEnsure
                result_workNetDictionaty['퇴직금지급방법_' + articleUniqueNum].replace("\t", ""),  # retirePay
                result_workNetDictionaty['접수마감일_' + articleUniqueNum].replace("\t", ""),  # applyDueDate
                result_workNetDictionaty['전형방법_' + articleUniqueNum].replace("\t", ""),  # howToRecruit_detl
                result_workNetDictionaty['접수방법_' + articleUniqueNum].replace("\t", ""),  # howToApply_detl
                result_workNetDictionaty['제출서류준비물_' + articleUniqueNum].replace("\t", ""),  # applyDoc
                result_workNetDictionaty['제출서류양식첨부_' + articleUniqueNum].replace("\t", ""),  # applyDocAttach
                result_workNetDictionaty['외국어능력_' + articleUniqueNum].replace("\t", ""),  # bilingual
                result_workNetDictionaty['전공_' + articleUniqueNum].replace("\t", ""),  # collgMajor
                result_workNetDictionaty['자격면허_' + articleUniqueNum].replace("\t", ""),  # license
                result_workNetDictionaty['컴퓨터활용능력_' + articleUniqueNum].replace("\t", ""),  # comCap
                result_workNetDictionaty['우대조건_' + articleUniqueNum].replace("\t", ""),  # prfrFactor_detl
                result_workNetDictionaty['병역특례채용희망_' + articleUniqueNum].replace("\t", ""),  # wichHireMil
                result_workNetDictionaty['장애인채용희망_' + articleUniqueNum].replace("\t", ""),  # wishHireDisabled
                result_workNetDictionaty['기타우대사항_' + articleUniqueNum].replace("\t", ""),  # etcPrefer
                result_workNetDictionaty['복리후생_' + articleUniqueNum].replace("\t", ""),  # welfare
                result_workNetDictionaty['장애인편의시설_' + articleUniqueNum].replace("\t", ""),  # facltDisabled
                result_workNetDictionaty['더추가할구인조건_' + articleUniqueNum].replace("\t", ""),  # moreHireCond
                result_workNetDictionaty['부서/담당자_' + articleUniqueNum].replace("\t", ""),  # recruitMngr
                result_workNetDictionaty['전화번호_' + articleUniqueNum].replace("\t", ""),  # recruitMngrTel1
                result_workNetDictionaty['휴대전화_' + articleUniqueNum].replace("\t", ""),  # recruitMngrTel2
                result_workNetDictionaty['팩스번호_' + articleUniqueNum].replace("\t", ""),  # faxNo
                result_workNetDictionaty['E-mail_' + articleUniqueNum].replace("\t", ""),  # recruitMngrEmail
                result_workNetDictionaty['기업종별_' + articleUniqueNum].replace("\t", ""),  #corpType
                result_workNetDictionaty['기업제시연봉_' + articleUniqueNum].replace("\t", ""),  # corpSuggWage
                result_workNetDictionaty['기업채용공고등록일_' + articleUniqueNum].replace("\t", ""),   #corpRegDate
                result_workNetDictionaty['기업평가글_' + articleUniqueNum].replace("\t", ""),       #corpEvalText
                result_workNetDictionaty['평균연봉_' + articleUniqueNum].replace("\t", "")    #avgYearWage
            )

            insertCnt = insertCnt + 1
            print('DB INSERT COUNT : ', insertCnt)
            self.logger.debug('DB INSERT COUNT : {}'.format(insertCnt))

            print('DB insert result : ', insertResult)
            self.logger.debug('DB insert result : {}'.format(insertResult))

            doneOrNot = True
        except Exception as e:
            print('데이터 입력 오류: ', e)
            doneOrNot = False

        return doneOrNot

    def couldScrolling(self, driver):
        ScrollTestResult = False

        try:
            driver.execute_script("return document.body.scrollHeight")

            print('스크롤이 가능한 페이지')
            self.logger.debug('스크롤이 가능한 페이지')

            ScrollTestResult = True

        except Exception as e_expArticle:
            print('can not do scroll', e_expArticle)
            self.logger.error('can not do scroll : {}'.format(e_expArticle))

        return ScrollTestResult

    # 상단에 인코딩을 명시적으로 표시해 줄 것 참조 : https://kyungw00k.github.io/2016/04/08/python-%ED%8C%8C%EC%9D%BC-%EC%83%81%EB%8B%A8%EC%97%90-%EC%BD%94%EB%93%9C-%EB%82%B4-%EC%9D%B8%EC%BD%94%EB%94%A9%EC%9D%84-%EB%AA%85%EC%8B%9C%EC%A0%81%EC%9C%BC%EB%A1%9C-%EC%B6%94%EA%B0%80%ED%95%A0-%EA%B2%83/
    def autoScroller(self, driver):
        # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
        SCROLL_PAUSE_TIME = 2

        # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
        autoScrolled_data_soup_html = ''
        last_height = driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            last_height = new_height

        # autoScroll crawling data 가져오기
        autoScrolled_data_soup_html = bs(driver.page_source, 'html.parser')
        return autoScrolled_data_soup_html

    def getTotalRecruitCount(self, driver):
        worknet_firstPage_soup_html = bs(driver.page_source, 'html.parser')

        totCnt_recruit = worknet_firstPage_soup_html.select("#searchCondExtVO > div.sub_search_wrap.matching2 > div.sch_total > span > em")[0].text.replace(",", "")

        print('전체 게시물 개수 : ', totCnt_recruit)
        self.logger.debug('전체 게시물 개수 : {}'.format(totCnt_recruit))

        return totCnt_recruit

    def getPagination(self, driver, searchURL):

        result_workNetDictionaty = {}
        page_url = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do?pageIndex={}"
        #http://www.work.go.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?searchInfoType=VALIDATION&callPage=detail&wantedAuthNo=KJNM001809060014&rtnTarget=list5&pageIndex=1&rtnUrl=/empInfo/empInfoSrch/list/dtlEmpSrchList.do?len=0&lastIndex=1&siteClcd=all&firstIndex=1&pageSize=10&recordCountPerPage=10&benefitSrchAndOr=O&srchJobNum=0&sortField=DATE&sortOrderBy=DESC&resultCnt=10&&empTpGbcd=1&onlyTitleSrchYn=N

        driver.get(page_url.format(1))
        totalCount_str = self.getTotalRecruitCount(driver)

        totalCount = int(totalCount_str)
        result_workNetDictionaty['전체게시물수'] = totalCount

        totalCount_page = int(totalCount/10) + 1

        self.logger.debug('전체 페이지 수: {}'.format(totalCount_page))
        print('전체 페이지 수 : ', totalCount_page)

        # 연결될 각 페이지의 URL
        dept_page_url = [page_url.format(i) for i in range(1, 3)]  # 페이지 수를 제한할 수 있음. 테스트를 위해 10페이지로 제한.
        #dept_page_url = [page_url.format(i) for i in range(1, totalCount_page)]

        # 기존 구인인증 번호 값 추출
        # 수집한 구인인증번호값은 현재까지 insert 된 데이터의 구인인증번호 값임.
        database_connection = mySQL_conn.DatabaseConnection_jeniel()
        returnedselectDataList = database_connection.select_record()

        # 각 페이지 정보 접근
        i = 0
        insertCnt = 0


        for page_length in range(len(dept_page_url)):

            insertCnt = 1
            try:
                driver.get(dept_page_url[i])

                i += 1
                self.logger.debug('current_url => {}'.format(driver.current_url))
                result_autoScroller = self.autoScroller(driver)

                # 각 공고별 정보 검색 및 취득
                for list_length in range(len(result_autoScroller.select("#searchCondExtVO > table > tbody > tr"))):
                    print('각 공고별 검색 start')
                    self.logger.debug('개별 공고 정보 검색 시작')
                    # 기업 명 체크박스 선별
                    # pageSourceText = result_autoScroller.find_all('input', {'id': 'chkboxWantedAuthNo' + list_indies.split(',')[list_length]} )

                    corpType = ''
                    corpFareFirst = ''
                    corpRegisterFirst = ''

                    # 마감된 채용정보 alert 발생 시 error 발생하는 try 문
                    try:
                        #201809추가
                        recruitUniqueNumber = '0000'
                        try:
                            #corpJobAltText = result_autoScroller.select("#list" + str(list_length + 1) + " > td:nth-of-type(2) > div:nth-of-type(1) > img").__getattribute__(self, 'alt')
                            #items = driver.find_element_by_tag_name('img')


                            corpInfoFirst = driver.find_element_by_xpath('//*[@id="list' + str(list_length + 1) + '"]/td[1]/input').get_attribute('value')
                            print('corpInfoFirst:', corpInfoFirst)

                            #K172121809070016|VALIDATION|(주)아산섬유|자동차 내장재 원단 생산직원 모집
                            try:
                                recruitUniqueNumber = corpInfoFirst.split("|")[0]
                            except Exception as e:
                                print('공고 리스트 전면부에 체크박스가 없음. 리스트 상에서 구인공고인증번호를 취득할 수 없음.', e)

                            corpNameFirst = driver.find_element_by_xpath('//*[@id="list' + str(list_length + 1) + '"]/td[2]/a').text
                            print('corpNameFirst:', corpNameFirst)

                            for corpTpelength in range(3):
                                try:
                                    print(driver.find_element_by_xpath('//*[@id="list' + str(list_length + 1) + '"]/td[2]/div[1]/img[' + str(corpTpelength + 1) + ']').get_attribute('alt'))
                                    corpType = driver.find_element_by_xpath('//*[@id="list' + str(list_length + 1) + '"]/td[2]/div[1]/img[' + str(corpTpelength + 1) + ']').get_attribute('alt')

                                    #result_workNetDictionaty['기업종별_' + recruitUniqueNumber] = corpType

                                except Exception as e:
                                    print('기업종별 구분값(벤처/가족/강소/대기업 등)이 존재하지 않음')

                                                                        #//*[@id="list3"]/td[5]/div[1]
                            corpFareFirst = driver.find_element_by_xpath('//*[@id="list' + str(list_length + 1) + '"]/td[4]/div').text.replace(" ", "")
                            print('corpFareFirst:', corpFareFirst)

                            #result_workNetDictionaty['기업제시연봉_' + recruitUniqueNumber] = corpFareFirst

                            corpRegisterFirst = driver.find_element_by_xpath('//*[@id="list' + str(list_length + 1) + '"]/td[5]/div').text
                            print('corpRegisterFirst:', corpRegisterFirst)

                            #result_workNetDictionaty['기업채용공고등록일_' + recruitUniqueNumber] = corpRegisterFirst


                        except Exception as e:
                            print('벤처/강소/가족 등의 표시 없음', e)
                            #corpType = '벤처/강소/가족 등의 표시 없음'
                            #result_workNetDictionaty['기업종별_' + recruitUniqueNumber] = corpType

                        corpJobText = result_autoScroller.select("#list" + str(list_length + 1) + " > td:nth-of-type(3) > dl > dt > a")[0].text

                        # beautifulsoup의 find 함수를 사용-> attr의  return 값을 dictionary 형태로 함.
                        corpJobText_URL = result_autoScroller.find("a", string=corpJobText)
                        # logger.debug('제목_URL : {}'.format(corpJobText_URL['href']) )

                        # 하단의 공고 세부항목으로 진입 후 출력되는 공고 제목과 비교하기 위함.
                        # corpJboArticleTitle = corpJobText.replace(
                        #     " ", "").replace(
                        #     "    ", "").replace(
                        #     "        ", "").replace(
                        #     "\n", "").replace(
                        #     "\xa0", "")

                        # 각 구인 공고별 URL 취득
                        corpJobText_detail_URL = corpJobText_URL['href']

                        # Maria-Field : 구인인증번호(구인공고고유값) : articleUniqueNum
                        articleOverViewInfo = result_autoScroller.find(id='chkboxWantedAuthNo' + str(list_length))['value']
                        self.logger.debug('구인인증번호|회사명|공고내용: {}'.format(articleOverViewInfo))

                        articleUniqueNum = articleOverViewInfo.split('|')[0]

                        # 구인인증 번호 취득 후, DB에서 articleUniqueNum만 받은 list와 값 비교를 하여 존재하는 값이면 다음 과정을 진행하지 않고,
                        # 존재하지 않는 값이면 다음 과정을 진행하도록 함.
                        print('구인인증번호 : ', articleUniqueNum)
                        self.logger.debug('구인인증번호: {}'.format(articleUniqueNum))

                        result_workNetDictionaty['기업종별_' + articleUniqueNum] = corpType
                        result_workNetDictionaty['기업제시연봉_' + articleUniqueNum] = corpFareFirst
                        result_workNetDictionaty['기업채용공고등록일_' + articleUniqueNum] = corpRegisterFirst


                        # 기 크롤링한 구인공고는 크롤링하지 않는다.
                        if articleUniqueNum in returnedselectDataList:
                            print('기 크롤링한 구인공고임.')
                            self.logger.debug('기 크롤링한 구인공고임. 구인인증번호: {}'.format(articleUniqueNum))
                            continue

                        # 한번도 크롤링 하지 않은 구인공고 정보를 가져온다.
                        # DB Insert가 실패하더라도 이는 기존의 공고라기 보다는 크롤링 과정 중 발생하는 중복에 의해 insert가 실패한 것이다.
                        else:
                            print('처음 크롤링하는 구인 공고임.')
                            self.logger.debug('처음 크롤링하는 취업 공고')
                            #corpNm1 = articleOverViewInfo.split('|')[1]
                            corpNm = articleOverViewInfo.split('|')[2]

                            # DATA : 구인인증번호: articleUniqueNum / 회사명: corpNm / 공고내용: corpWantJob
                            result_workNetDictionaty['구인인증번호_' + articleUniqueNum] = articleUniqueNum
                            result_workNetDictionaty['회사명_' + articleUniqueNum] = corpNm

                            # 구인 인증번호를 DB 검색하여 존재하는 인증번호이면 정보 취득 skip : 구인인증번호 SELECT 하여 이 값을 list로 만들고, 이를 가지고 기존 구인인증번호인지를 검색할 예정.
                            # No.1 세부 공고 내부로 진입
                            driver.get('http://www.work.go.kr' + corpJobText_detail_URL)

                            returnedPossibleScroll = self.couldScrolling(driver)
                            print('단순 스크롤이 가능한지 여부 확인 : ', returnedPossibleScroll)

                            # Scroll Test Success
                            if returnedPossibleScroll == True:

                                corpJobDetailArticle = self.autoScroller(driver)

                                # Maria-Field : 공고 제목 : corpRecruitArticleTitle
                                # Maria-Data : corpRecruitArticleTitle
                                corpRecruitArticleTitle = corpJobDetailArticle.select('div#content-area > div > div:nth-of-type(3) > h3')[
                                    0].text.replace(
                                    " ", " ").replace(
                                    "    ", " ").replace(
                                    "        ", " ").replace(
                                    "\n", "").replace(
                                    "\xa0", "").split("이메일입사지원")[0]

                                result_workNetDictionaty['공고제목_' + articleUniqueNum] = corpRecruitArticleTitle

                                #기업 정보 취득 함수
                                returnGongo = self.getAllGongoInfo(corpJobDetailArticle, result_workNetDictionaty, articleUniqueNum)
                                print('get All Gongo Info :', returnGongo)

                                # if returnGongo == True:
                                #     print('채용정보를 성공적으로 취득하였음.')
                                #     #채용정보에서 기업정보로 넘어감.
                                #     try:
                                #         link = self.driver.find_element_by_xpath('//*[@id="content-area"]/div/ul/li[2]/a')
                                #         link.click()
                                #
                                #         print(self.driver.current_url)
                                #
                                #         self.getCorpDetailInfo(driver, self.driver.current_url, articleUniqueNum, result_workNetDictionaty)
                                #
                                #     except Exception as e:
                                #         print('기업 정보 탭이 존재하지 않습니다.', e)
                                #
                                #
                                #
                                # else:
                                #     print('채용정보를 정상적으로 취득하지 못함.')
                                #     #기업 정보로 넘어감
                                #     try:
                                #         link = self.driver.find_element_by_xpath('//*[@id="content-area"]/div/ul/li[2]/a')
                                #         link.click()
                                #
                                #         print(self.driver.current_url)
                                #
                                #         self.getCorpDetailInfo(driver, self.driver.current_url, articleUniqueNum, result_workNetDictionaty)
                                #
                                #     except Exception as e:
                                #         print('기업 정보 탭이 존재하지 않습니다.', e)


                            else:
                                print('정상적으로 스크롤을 진행할 수 있는 화면이 아닙니다. 아마도, 마감된 채용 정보일 것입니다.다음 정보로 넘어갑니다.')
                                # 다음 loop로 넘어간다.

                                alertObj = driver.switch_to_alert()
                                alertObj.accept()
                                continue

                    except Exception as e_url:
                        print('마감된 채용정보 알림창이 떴습니다 :', e_url)
                        result_workNetDictionaty['회사명_' + articleUniqueNum] = ''
                        result_workNetDictionaty['공고제목_' + articleUniqueNum] = ''
                        # result_workNetDictionaty['공고제목상세_' + articleUniqueNum] = ''
                        result_workNetDictionaty['조회수_' + articleUniqueNum] = ''
                        result_workNetDictionaty['지원자_' + articleUniqueNum] = ''
                        result_workNetDictionaty['corpImgDir_' + articleUniqueNum] = ''
                        result_workNetDictionaty['회사명_' + articleUniqueNum] = ''
                        result_workNetDictionaty['대표자명_' + articleUniqueNum] = ''
                        result_workNetDictionaty['근로자수_' + articleUniqueNum] = ''
                        result_workNetDictionaty['자본금_' + articleUniqueNum] = ''
                        result_workNetDictionaty['연매출액_' + articleUniqueNum] = ''
                        result_workNetDictionaty['업종_' + articleUniqueNum] = ''
                        result_workNetDictionaty['주요사업내용_' + articleUniqueNum] = ''
                        result_workNetDictionaty['회사주소_' + articleUniqueNum] = ''
                        result_workNetDictionaty['홈페이지_' + articleUniqueNum] = ''
                        result_workNetDictionaty['모집직종_' + articleUniqueNum] = ''
                        result_workNetDictionaty['직종키워드_' + articleUniqueNum] = ''
                        result_workNetDictionaty['관련직종_' + articleUniqueNum] = ''
                        result_workNetDictionaty['직무내용_' + articleUniqueNum] = ''
                        result_workNetDictionaty['경력조건_' + articleUniqueNum] = ''
                        result_workNetDictionaty['학력_' + articleUniqueNum] = ''
                        result_workNetDictionaty['근무지역_' + articleUniqueNum] = ''
                        result_workNetDictionaty['임금_' + articleUniqueNum] = ''
                        result_workNetDictionaty['고용형태_' + articleUniqueNum] = ''
                        result_workNetDictionaty['모집인원_' + articleUniqueNum] = ''
                        result_workNetDictionaty['근무예정지_' + articleUniqueNum] = ''
                        result_workNetDictionaty['소속산업단지_' + articleUniqueNum] = ''
                        result_workNetDictionaty['인근전철역_' + articleUniqueNum] = ''
                        result_workNetDictionaty['임금조건_' + articleUniqueNum] = ''
                        # result_workNetDictionaty['식사(비)제공_' + articleUniqueNum] = ''
                        result_workNetDictionaty['근무시간_' + articleUniqueNum] = ''
                        result_workNetDictionaty['근무형태_' + articleUniqueNum] = ''
                        result_workNetDictionaty['사회보험_' + articleUniqueNum] = ''
                        result_workNetDictionaty['퇴직금지급방법_' + articleUniqueNum] = ''
                        result_workNetDictionaty['접수마감일_' + articleUniqueNum] = ''
                        result_workNetDictionaty['전형방법_' + articleUniqueNum] = ''
                        result_workNetDictionaty['접수방법_' + articleUniqueNum] = ''
                        result_workNetDictionaty['제출서류준비물_' + articleUniqueNum] = ''
                        result_workNetDictionaty['제출서류양식첨부_' + articleUniqueNum] = ''
                        result_workNetDictionaty['외국어능력_' + articleUniqueNum] = ''
                        result_workNetDictionaty['전공_' + articleUniqueNum] = ''
                        result_workNetDictionaty['자격면허_' + articleUniqueNum] = ''
                        result_workNetDictionaty['컴퓨터활용능력_' + articleUniqueNum] = ''
                        result_workNetDictionaty['우대조건_' + articleUniqueNum] = ''
                        result_workNetDictionaty['병역특례채용희망_' + articleUniqueNum] = ''
                        result_workNetDictionaty['장애인채용희망_' + articleUniqueNum] = ''
                        result_workNetDictionaty['기타우대사항_' + articleUniqueNum] = ''
                        result_workNetDictionaty['복리후생_' + articleUniqueNum] = ''
                        result_workNetDictionaty['장애인편의시설_' + articleUniqueNum] = ''
                        result_workNetDictionaty['더추가할구인조건_' + articleUniqueNum] = ''
                        result_workNetDictionaty['부서/담당자_' + articleUniqueNum] = ''
                        result_workNetDictionaty['전화번호_' + articleUniqueNum] = ''
                        result_workNetDictionaty['휴대전화_' + articleUniqueNum] = ''
                        result_workNetDictionaty['팩스번호_' + articleUniqueNum] = ''
                        result_workNetDictionaty['E-mail_' + articleUniqueNum] = ''
                        result_workNetDictionaty['기업종별_' + articleUniqueNum] = ''
                        result_workNetDictionaty['기업제시연봉_' + articleUniqueNum] = ''
                        result_workNetDictionaty['기업채용공고등록일_' + articleUniqueNum] = ''
                        result_workNetDictionaty['기업평가글_' + articleUniqueNum] = ''

                        continue

            except Exception as e_magam:
                print('마감된 채용 정보입니다.', e_magam)
                self.logger.error('마감된 채용 정보입니다 : {} '.format(e_magam))

                alertObj = driver.switch_to_alert()
                alertObj.accept()

                continue

        print('Final_Data : ', result_workNetDictionaty)
        return result_workNetDictionaty

    def bringContentBasicData(self, driver, searchURL):
        driver.get(searchURL)
        crawledResults = self.getPagination(driver, searchURL)

        return crawledResults

    def setLog(self):
        # logger 인스턴스를 생성 및 로그 레벨 설정

        self.logger.setLevel(logging.DEBUG)

        # formatter 생성
        formatter = logging.Formatter('[%(levelname)s|%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

        # fileHandler와 StreamHandler를 생성
        file_max_bytes = 10 * 1024 * 1024  # log file size : 10MB
        fileHandler = logging.handlers.RotatingFileHandler("./log/" + self.hereWork + "_on_" + self.currTime, maxBytes=file_max_bytes,  encoding='UTF-8', backupCount=10)
        streamHandler = logging.StreamHandler()

        # handler에 fommater 세팅
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)

        # Handler를 logging에 추가
        self.logger.addHandler(fileHandler)

        # def CrawlingByWorkNetCrawlBot():
        start_time_all = time.time()

    def setUp(self):
        #self.driver = webdriver.Firefox(firefox_binary = self.binary)

        self.chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=1920x1080")

        self.prefs = {}
        self.prefs['profile.default_content_setting_values.notifications'] = 2
        self.chrome_options.add_experimental_option('prefs', self.prefs)
        self.driver_chrome = "C:\\dev_tenspace\\PycharmProjects\\aster_dev_201808\\chromedriver.exe"

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.driver_chrome)


    def worknet_login(self):
        self.setUp()
        driver = self.driver

        userid = 'microscope83'
        userpw = 'Gkstkddbs1!'

        visitedURL = "http://www.work.go.kr/seekWantedMain.do"
        driver.get(visitedURL)

        if driver.find_element_by_id('chkKeyboard').is_selected():
            print('get in')
            driver.execute_script("arguments[0].click();", driver.find_element_by_id('chkKeyboard'))

            driver.find_element_by_id('custId').send_keys(userid)
            driver.find_element_by_id('pwd').send_keys(userpw)

            driver.find_element_by_id('btnLogin').click()
            print(driver.current_url)
            print('login success')


            searchURL = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"
            returnResult = self.bringContentBasicData(driver, searchURL)


            driver.get(searchURL)
            print('최종 수집 데이터 결과 출력: ', returnResult)

            driver.close()

        else:
            print('키보드 보안 프로그램으로 인해 해결 불가')
            print('login failed')

            #http://www.work.go.kr/empInfo/empInfoSrch/detail/empDetailAuthView.do?wantedAuthNo=K151221809060002&iorgGbcd=
            searchURL = "http://www.work.go.kr/empInfo/empInfoSrch/list/dtlEmpSrchList.do"
            returnResult = self.bringContentBasicData(driver, searchURL)
            driver.get(searchURL)
            print('최종 수집 데이터 결과 출력: ', returnResult)

            driver.close()

if __name__ == "__main__":
    worknetPrj = worknetCrawlerBot()
    worknetPrj.worknet_login()
