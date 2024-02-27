# One time creation file

import MySQLdb
hostName = 'db4free.net'      
userName = 'udreedbczu'          
passWord = 'ezcb9vazqz'           
dbName =  userName                
DBConn= MySQLdb.connect(hostName,userName,passWord,dbName)
def runCMD (DDL):
    DBConn= MySQLdb.connect(hostName,userName,passWord,dbName)
    myCursor = DBConn.cursor()
    retcode = myCursor.execute(DDL) 
    print (retcode)
    DBConn.commit()
    DBConn.close()

def runSELECT (CMD):
    DBConn= MySQLdb.connect(hostName,userName,passWord,dbName)
    df_mysql = pd.read_sql(CMD, con=DBConn)    
    DBConn.close()
    return df_mysql

def r(msg):
    if msg[0:6]=="SELECT" or msg[0:6]=="select":
        return runSELECT(msg)
    else:
        runCMD(msg)

"""

Create table for storing aspirant email IDs and topics

"""

r('DROP TABLE if exists aspirant_topics')        
r("CREATE TABLE aspirant_topics( \
login varchar(70) not null, \
topics varchar(500) not null)")