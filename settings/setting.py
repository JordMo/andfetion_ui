import pymysql, datetime
import os
MYSQL_CONF = ['127.0.0.1', 'root', 'root', 'andfetion_ui', "utf8"]

def connect_db():
    conn = pymysql.connect(
        host=MYSQL_CONF[0],
        user=MYSQL_CONF[1],
        password=MYSQL_CONF[2],
        database=MYSQL_CONF[3],
        charset=MYSQL_CONF[4]
    )
    print("连接数据库成功")
    cursor = conn.cursor()
    return conn, cursor

def get_app_version(apppackage="com.chinasofti.rcs"):
    try:
        if isWindows():
            result = os.popen('adb shell pm dump %s | findstr versionName'%apppackage)
            name, value = result.read().strip().split('=')
            return value
        output = os.popen('adb shell pm dump %s|grep versionName' %apppackage)
        output =output.read().replace("versionName=","")
        output =output.replace(" ","")
        output =output.replace("\n","")      
    except:       
        output="6.3.1.0528"
    return output


def isWindows():
    """判断平台为windows还是linux"""
    import platform
    sysstr = platform.system()
    if (sysstr == "Windows"):
        return True
    return False

if __name__ == '__main__':
    print(get_app_version())
