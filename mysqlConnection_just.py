
#!/usr/bin/python
import pymysql

'''
Python에서 MySQL에 있는 데이타를 사용하는 일반적인 절차는 다음과 같다.

1. PyMySql 모듈을 import 한다
2. pymysql.connect() 메소드를 사용하여 MySQL에 Connect 한다. 호스트명, 로그인, 암호, 접속할 DB 등을 파라미터로 지정한다.
3. DB 접속이 성공하면, Connection 객체로부터 cursor() 메서드를 호출하여 Cursor 객체를 가져온다. DB 커서는 Fetch 동작을 관리하는데 사용되는데, 만약 DB 자체가 커서를 지원하지 않으면, Python DB API에서 이 커서 동작을 Emulation 하게 된다.
4. Cursor 객체의 execute() 메서드를 사용하여 SQL 문장을 DB 서버에 보낸다.
5. SQL 쿼리의 경우 Cursor 객체의 fetchall(), fetchone(), fetchmany() 등의 메서드를 사용하여 데이타를 서버로부터 가져온 후, Fetch 된 데이타를 사용한다.
6. 삽입, 갱신, 삭제 등의 DML(Data Manipulation Language) 문장을 실행하는 경우, INSERT/UPDATE/DELETE 후 Connection 객체의 commit() 메서드를 사용하여 데이타를 확정 갱신한다.
7. Connection 객체의 close() 메서드를 사용하여 DB 연결을 닫는다.
'''


class DatabaseConnection_jeniel:
    def __init__(self):

        try:
            self.connection = pymysql.connect(host='uml.kr', port=3366,
                       user='just_aster_dba', password='!just716811',
                       db='just', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            print('DB connection completed')

        except:
            print('Cannot connect to Database')

    def create_worknet_table(self):
        create_table_query = "CREATE TABLE 'just_crawled_worknet' (\
                                'no_index' INT(11) NOT NULL AUTO_INCREMENT COMMENT 'index',\
                                'articleUniqueNum' VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '구인인증번호',\
                                'corpNm' VARCHAR(50) NULL DEFAULT '0' COMMENT '리스트상의 회사이름',\
                                'corpWantJob' VARCHAR(50) NULL DEFAULT '0' COMMENT '리스트상의 공고내용(제목이 포함될 수 있음)',\
                                'corpRecruitArticleTitle' VARCHAR(50) NULL DEFAULT '0' COMMENT '리스트상의 공고제목',\
                                'searchArticleCnt' VARCHAR(50) NULL DEFAULT '0' COMMENT '공고조회수',\
                                'applicantArticleCnt' VARCHAR(50) NULL DEFAULT '0' COMMENT '공고지원자수',\
                                'corpImgDir' VARCHAR(300) NULL DEFAULT '0' COMMENT '회사이미지사용유무',\
                                'corpNm_detl' VARCHAR(50) NULL DEFAULT '0' COMMENT '회사명',\
                                'ceoNm' VARCHAR(50) NULL DEFAULT '0' COMMENT '대표자명',\
                                'workerCnt' VARCHAR(100) NULL DEFAULT '0' COMMENT '근로자수',\
                                'jabon' VARCHAR(50) NULL DEFAULT '0' COMMENT '자본금',\
                                'yearIncome' VARCHAR(50) NULL DEFAULT '0' COMMENT '연매출액',\
                                'jobKind' VARCHAR(150) NULL DEFAULT '0' COMMENT '업종',\
                                'jobKind_main' VARCHAR(150) NULL DEFAULT '0' COMMENT '주요사업내용',\
                                'corpAddr' VARCHAR(150) NULL DEFAULT '0' COMMENT '회사주소',\
                                'homepage' VARCHAR(100) NULL DEFAULT '0' COMMENT '홈페이지',\
                                'recruitJobKind' VARCHAR(50) NULL DEFAULT '0' COMMENT '모집직종',\
                                'jobKindKeyword' VARCHAR(50) NULL DEFAULT '0' COMMENT '직종키워드',\
                                'relatedJobKind' VARCHAR(50) NULL DEFAULT '0' COMMENT '관련직종',\
                                'whatWork' VARCHAR(300) NULL DEFAULT '0' COMMENT '직무내용',\
                                'experOpt' VARCHAR(50) NULL DEFAULT '0' COMMENT '경력조건',\
                                'eduCond' VARCHAR(100) NULL DEFAULT '0' COMMENT '학력',\
                                'workArea' VARCHAR(50) NULL DEFAULT '0' COMMENT '근무지역',\
                                'wageCond' VARCHAR(50) NULL DEFAULT '0' COMMENT '임금',\
                                'hireType_detl' VARCHAR(50) NULL DEFAULT '0' COMMENT '고용형태',\
                                'hireCnt' VARCHAR(300) NULL DEFAULT '0' COMMENT '모집인원',\
                                'workPlace' VARCHAR(50) NULL DEFAULT '0' COMMENT '근무예정지',\
                                'industCommnt' VARCHAR(50) NULL DEFAULT '0' COMMENT '소속산업단지',\
                                'nearSubway' VARCHAR(100) NULL DEFAULT '0' COMMENT '인근전철역',\
                                'wageCond_detl' VARCHAR(100) NULL DEFAULT '0' COMMENT '임금조건',\
                                'mealOffer' VARCHAR(100) NULL DEFAULT '0' COMMENT '식사(비)제공',\
                                'workTime' VARCHAR(300) NULL DEFAULT '0' COMMENT '근무시간',\
                                'jobType' VARCHAR(100) NULL DEFAULT '0' COMMENT '근무형태',\
                                'socialEnsure' VARCHAR(100) NULL DEFAULT '0' COMMENT '사회보험',\
                                'retirePay' VARCHAR(50) NULL DEFAULT '0' COMMENT '퇴직금지급방법',\
                                'applyDueDate' VARCHAR(100) NULL DEFAULT '0' COMMENT '접수마감일',\
                                'howToRecruit_detl' VARCHAR(350) NULL DEFAULT '0' COMMENT '전형방법',\
                                'howToApply_detl' VARCHAR(350) NULL DEFAULT '0' COMMENT '접수방법',\
                                'applyDoc' VARCHAR(150) NULL DEFAULT '0' COMMENT '제출서류준비물',\
                                'applyDocAttach' VARCHAR(350) NULL DEFAULT '0' COMMENT '제출서류양식첨부',\
                                'bilingual' VARCHAR(50) NULL DEFAULT '0' COMMENT '외국어능력',\
                                'collgMajor' VARCHAR(50) NULL DEFAULT '0' COMMENT '전공',\
                                'license' VARCHAR(150) NULL DEFAULT '0' COMMENT '자격면허',\
                                'comCap' VARCHAR(150) NULL DEFAULT '0' COMMENT '컴퓨터활용능력',\
                                'prfrFactor_detl' VARCHAR(50) NULL DEFAULT '0' COMMENT '우대조건',\
                                'wishHireMil' VARCHAR(50) NULL DEFAULT '0' COMMENT '병역특례채용희망',\
                                'wishHireDisabled' VARCHAR(50) NULL DEFAULT '0' COMMENT '장애인채용희망',\
                                'etcPrefer' VARCHAR(50) NULL DEFAULT '0' COMMENT '기타우대사항',\
                                'welfare' VARCHAR(350) NULL DEFAULT '0' COMMENT '복리후생',\
                                'facltDisabled' VARCHAR(100) NULL DEFAULT '0' COMMENT '장애인편의시설',\
                                'moreHireCond' VARCHAR(150) NOT NULL DEFAULT '0' COMMENT '더 추가할 구인 조건',\
                                'recruitMngr' VARCHAR(100) NOT NULL DEFAULT '0' COMMENT '부서/담당자',\
                                'recruitMngrTel1' VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '전화번호',\
                                'recruitMngrTel2' VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '휴대전화',\
                                'faxNo' VARCHAR(50) NOT NULL DEFAULT '0' COMMENT '팩스번호',\
                                'recruitMngrEmail' VARCHAR(100) NOT NULL DEFAULT '0' COMMENT '이메일',\
                                PRIMARY KEY ('no_index','articleUniqueNum')\
                            )\
                            COLLATE='utf8_general_ci'\
                            ENGINE=InnoDB\
                            AUTO_INCREMENT=18\
                            ;\
                            "

        self.cursor.execute(create_table_query)
        self.connection.close()

    def insert_new_record(self, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10,
                          f11, f12, f13, f14, f15, f16, f17, f18, f19, f20,
                          f21, f22, f23, f24, f25, f26, f27, f28, f29, f30,
                          f31, f32, f33, f34, f35, f36, f37, f38, f39, f40,
                          f41, f42, f43, f44, f45, f46, f47, f48, f49, f50,
                          f51, f52, f53, f54, f55, f56, f57, f58, f59, f60):
                            #f56 삭제

        dbInsertResult = False

        try:
            # insert_command = "INSERT INTO just_crawled_worknet(articleUniqueNum, corpNm," \
            #                  " corpWantJob, corpRecruitArticleTitle, searchArticleCnt, applicantArticleCnt," \
            #                  " corpImgDir, corpNm_detl, ceoNm, workerCnt, jabon, yearIncome, jobKind, jobKind_main," \
            #                  " corpAddr, homepage, recruitJobKind, jobKindKeyword, relatedJobKind, whatWork, experOpt, " \
            #                  " eduCond, workArea, wageCond, hireType_detl, hireCnt, workPlace, industCommnt," \
            #                  " nearSubway, wageCond_detl, mealOffer, workTime, jobType, socialEnsure, retirePay, applyDueDate, howToRecruit_detl, howToApply_detl," \
            #                  " applyDoc, applyDocAttach, bilingual, collgMajor, license, comCap, prfrFactor_detl, wishHireMil, wishHireDisabled," \
            #                  " etcPrefer, welfare, facltDisabled, moreHireCond, recruitMngr, recruitMngrTel1, recruitMngrTel2, faxNo, recruitMngrEmail) " \
            #                  "VALUES ('" + f1 + "','" + f2 + "','" + f3 + "','" + f4 + "','" + f5 + "','" + \
            #                  f6 + "','" + f7 + "','" + f8 + "','" + f9 + "','" + f10 + "','" + \
            #                  f11 + "','" + f12 + "','" + f13 + "','" + f14 + "','" + f15 + "','" + \
            #                  f16 + "','" + f17 + "','" + f18 + "','" + f19 + "','" + f20 + "','" + \
            #                  f21 + "','" + f22 + "','" + f23 + "','" + f24 + "','" + f25 + "','" + \
            #                  f26 + "','" + f27 + "','" + f28 + "','" + f29 + "','" + f30 + "','" + \
            #                  f31 + "','" + f32 + "','" + f33 + "','" + f34 + "','" + f35 + "','" + \
            #                  f36 + "','" + f37 + "','" + f38 + "','" + f39 + "','" + f40 + "','" + \
            #                  f41 + "','" + f42 + "','" + f43 + "','" + f44 + "','" + f45 + "','" + \
            #                  f46 + "','" + f47 + "','" + f48 + "','" + f49 + "','" + f50 + "','" + \
            #                  f51 + "','" + f52 + "','" + f53 + "','" + f54 + "','" + f55 + "','" + \
            #                  f56 + "')"

            #공고 제목 상세 제거 : corpRecruitArticleTitle
            insert_command2 = "INSERT INTO just_crawled_worknet(articleUniqueNum, corpNm," \
                             " corpWantJob, searchArticleCnt, applicantArticleCnt," \
                             " corpImgDir, corpNm_detl, ceoNm, workerCnt, jabon, yearIncome, jobKind, jobKind_main," \
                             " corpAddr, homepage, recruitJobKind, jobKindKeyword, relatedJobKind, whatWork, experOpt, " \
                             " eduCond, workArea, wageCond, hireType_detl, hireCnt, workPlace, industCommnt," \
                             " nearSubway, wageCond_detl, mealOffer, workTime, jobType, socialEnsure, retirePay, applyDueDate, howToRecruit_detl, howToApply_detl," \
                             " applyDoc, applyDocAttach, bilingual, collgMajor, license, comCap, prfrFactor_detl, wishHireMil, wishHireDisabled," \
                             " etcPrefer, welfare, facltDisabled, moreHireCond, recruitMngr, recruitMngrTel1, recruitMngrTel2, faxNo, recruitMngrEmail, " \
                             "comScale, corpSuggWage, corpRegDate, corpEvalText, avgYearWage) " \
                             "VALUES ('" + f1 + "','" + f2 + "','" + f3 + "','" + f4 + "','" + f5 + "','" + \
                             f6 + "','" + f7 + "','" + f8 + "','" + f9 + "','" + f10 + "','" + \
                             f11 + "','" + f12 + "','" + f13 + "','" + f14 + "','" + f15 + "','" + \
                             f16 + "','" + f17 + "','" + f18 + "','" + f19 + "','" + f20 + "','" + \
                             f21 + "','" + f22 + "','" + f23 + "','" + f24 + "','" + f25 + "','" + \
                             f26 + "','" + f27 + "','" + f28 + "','" + f29 + "','" + f30 + "','" + \
                             f31 + "','" + f32 + "','" + f33 + "','" + f34 + "','" + f35 + "','" + \
                             f36 + "','" + f37 + "','" + f38 + "','" + f39 + "','" + f40 + "','" + \
                             f41 + "','" + f42 + "','" + f43 + "','" + f44 + "','" + f45 + "','" + \
                             f46 + "','" + f47 + "','" + f48 + "','" + f49 + "','" + f50 + "','" + \
                             f51 + "','" + f52 + "','" + f53 + "','" + f54 + "','" + f55 + "','" + \
                             f56 + "','" + f57 + "','" + f58 + "','" + f59 + "','" + f60 + "')"



            print(insert_command2)
            self.cursor.execute(insert_command2)

            self.connection.commit()
            self.connection.close()

            dbInsertResult = True

            return dbInsertResult

        except Exception as e:
            print('DBINSERT_FALSE', e)

            return dbInsertResult


    def select_record(self):
        try:
            selectedDataList = []
            self.cursor.execute("select no_index, articleUniqueNum from just_crawled_worknet order by no_index ASC;")
            cats = self.cursor.fetchall()
            for cat in cats:
                print('index + 구인인증번호: ', cat)
                
                #articleUniqueNum 만 list 에 넣기 위함
                selectedDataList.append(cat[1])
                #print("each rows : {}".format(cat))

            self.connection.close()

            return selectedDataList

        except Exception as e:
            print('select_record -> ', e)
            return None
        
        
'''
if __name__ == '__main__':
    database_connection = DatabaseConnection()
    #database_connection.create_table()
    database_connection.insert_new_record()
    database_connection.query_all()
'''