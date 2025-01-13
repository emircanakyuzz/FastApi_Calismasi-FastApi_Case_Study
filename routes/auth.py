import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from schemas import LoginUser
from database import get_database_connection
from mysql.connector import Error

router = APIRouter() # APIRouter nesnesini oluşturalım

@router.post("/login")
async def login_user(user: LoginUser):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("SELECT * FROM users WHERE mail = %s AND password = %s", (user.mail, user.password))
        existing_user = db_cursor.fetchone()
        if not existing_user:
            raise HTTPException(status_code=400, detail="Mail veya şifre hatalı")
        else:
            return {"message": existing_user}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()