import mysql.connector as MySQLdb
# from pandas.io import sql
import datetime

class DBUtil:
    p_time =[]
    bidO = []
    askO = []
    bidB = []
    askB = []

    def getData(self):

        # conn = MySQLdb.connect(host="localhost", user="root",
        #                           passwd="", db="Arbitrage")
        # query = "SELECT * from Statistics_Prices ORDER by p_time desc"
        #
        # results = sql.read_sql(query, con=conn)
        #
        # print results

        db = MySQLdb.connect(host="localhost", user="root",
                                  passwd="", db="Arbitrage")
        cursor = db.cursor()

        try:
            # execute SQL query using execute() method.
            cursor.execute("SELECT * from Statistics_Prices ORDER by p_time desc")
            results = cursor.fetchmany(size=420)
            for row in reversed(results):
                self.p_time.append(datetime.datetime.strftime(row[0],'%Y-%m-%d %H:%M:%S'))
                self.bidO.append(round(row[1],ndigits=4))
                self.askO.append(row[2])
                self.bidB.append(row[3])
                self.askB.append(round(row[4],ndigits=4))
        except:
            print("Error: unable to fecth data")
        db.close()
        return results

    # def exportData(self,data):
    #     db = MySQLdb.connect(host="localhost", user="root",
    #                               passwd="", db="Arbitrage")
    #     cursor = db.cursor()
    #     sql = "INSERT INTO EMPLOYEE(, \
    #     LAST_NAME, AGE, SEX, INCOME) \
    #     VALUES ('%s', '%s', '%d', '%c', '%d' )" % \
    #     ('Mac', 'Mohan', 20, 'M', 2000)
    #
    #
    #
    #
    #     db.close()
