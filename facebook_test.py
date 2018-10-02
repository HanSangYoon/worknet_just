import csv
import logging.handlers
import time

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

#https://www.facebook.com/hyoungwoo.kim.zermatt/about?lst=100006841668710
'''
def autoScrollerInformationTAB(driver):
    # 게시글에서 좋아요 표시 갯수, 댓글 수 등의 정보 추출 >>  AUTO SCROLL 기능 필요
    SCROLL_PAUSE_TIME = 0.5

    # 화면 길이 만큼 나눠 autoScroll 하고 각 페이지마다 데이터 가져오기
    autoScrolled_data_soup_html = ''
    last_height = driver.execute_script("return document.body.scrollHeight")

    # 화면 사이즈 생성하기(15번의 새로고침이 있을 정도로만 데이터 추출)
    for cyc in range(0, 6):
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


    try:
        time.sleep(2)

        medley_header_list = ['pagelet_timeline_medley_about', 'medley_header_friends', 'pagelet_timeline_medley_photos', ]


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


#if __name__ == "__main__":

'''