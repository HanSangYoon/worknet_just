import pymysql


class DatabaseConnection_origin:
    def __init__(self):

        try:

            # SCI
            '''
            self.connection = pymysql.connect(host='172.16.4.158',
                       user='aster_sci_add', password='!sci716811',
                       db='aster_sci', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            '''
            '''
            #localhost
            self.connection = pymysql.connect(host='localhost',
                       user='aster_dba', password='!sci716811',
                       db='aster_sci', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()


                        #localhost
            self.connection = pymysql.connect(host='localhost',
                       user='aster_dba', password='!sci716811',
                       db='aster', charset='utf8')

            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            '''
            # localhost
            self.connection = pymysql.connect(host='uml.kr', port=3366,
                                              user='just_aster_dba', password='!just716811',
                                              db='just', charset='utf8')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

            print('DB connection completed')

        except:
            print('Cannot connect to Database')


if __name__ == "__main__":
    databaseConn = DatabaseConnection_origin()

    databaseConn