import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from schemas import CreateUser, UpdateUser, RetrieveUser, DeleteUser
from database import get_database_connection
from mysql.connector import Error

router = APIRouter()

# Kullanıcı kayıt işlemi
@router.post("/register")
async def create_user(user: CreateUser):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("SELECT * FROM users WHERE mail = %s", (user.mail,))
        existing_user = db_cursor.fetchone()
        
        if not existing_user:
            sql = "INSERT INTO users (name, surname, mail, password, date, sex) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (user.name, user.surname, user.mail, user.password, user.date, user.sex)
            db_cursor.execute(sql, values)
            db_connection.commit()
            return {"message": "Kullanıcı başarıyla kaydedildi!"}
        else:
            raise HTTPException(status_code=400, detail="Bu mail adresi ile kayıtlı kullanıcı mevcut")
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()

# Kullanıcı görüntüleme / getirme işlemi
@router.get("/get/{user_id}")
async def get_user(user_id: int):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = db_cursor.fetchone()
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        else:
            return {"user": existing_user}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()

# Kullanıcı güncelleme işlemi
@router.patch("/update/{user_id}")
async def update_user(user_id: int, user: UpdateUser):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = db_cursor.fetchone()
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
        else:
            user_dict = user.dict()
            for key, value in user_dict.items():
                if value:
                    sql = f"UPDATE users SET {key} = %s WHERE id = %s"
                    values = (value, user_id)
                    db_cursor.execute(sql, values)
                    db_connection.commit()
            return {"message": f"Kullanıcı başarıyla güncellendi! Güncellenmiş veri: {str(user)}"}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()
        
# Kullanıcı silme işlemi
@router.delete("/delete/{user_id}")
async def delete_user(user_id: int):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        # Kullanıcı kontrolü
        db_cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        existing_user = db_cursor.fetchone()
        if not existing_user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

        # Kullanıcıyı sil
        db_cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        db_connection.commit()
        
        # id sütununu yeniden sıralıyoruz
        db_cursor.execute("SET @count = 0;")
        db_cursor.execute("UPDATE users SET id = @count:= @count + 1;")
        db_cursor.execute("ALTER TABLE users AUTO_INCREMENT = 1;")
        db_connection.commit()
        
        return {"message": "Kullanıcı silindi! Silinen kullanıcı:" + str(existing_user)}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()