import pymysql

def get_connection():
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="goku",
        database="education_analysis"
    )

    return conn