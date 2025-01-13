from fastapi import HTTPException
import mysql.connector as mysql
from mysql.connector import Error

def get_database_connection():
    try:
        db_connection = mysql.connect(
            host="localhost",
            user="root",
            password="",
            database="finale"
        )
        return db_connection
    
    except Error as db_error:
        print(f"Veri tabanaı bağlantısı başarısız {db_error}")
        raise (HTTPException(status_code = 500, detail = "Veri tabanı bağlantısı başarısız"))