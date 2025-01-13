import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from schemas import CreatePost, RetrievePost, UpdatePost, DeletePost
from database import get_database_connection
from mysql.connector import Error

router = APIRouter()

# Gönderi oluşturma işlemi
@router.post("/create")
async def create_post(post: CreatePost):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        sql = "INSERT INTO posts (title, contents, date) VALUES (%s, %s, %s)"
        values = (post.title, post.contents, post.date)
        db_cursor.execute(sql, values)
        db_connection.commit()
        return {"message": "Gönderi başarıyla oluşturuldu!"}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()

# Gönderi görüntüleme işlemi
@router.get("/get/{post_id}")
async def get_post(post_id: int):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
        existing_post = db_cursor.fetchone()
        
        if not existing_post:
            raise HTTPException(status_code=404, detail="Gönderi bulunamadı")
        else:
            return {"post": existing_post}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()

# Tüm gönderileri listeleme işlemi
@router.get("/all")
async def get_all_posts():
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("SELECT * FROM posts ORDER BY post_id DESC")
        posts = db_cursor.fetchall()
        
        return {"posts": posts}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()

# Gönderi güncelleme işlemi
@router.patch("/update/{post_id}")
async def update_post(post_id: int, post: UpdatePost):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        db_cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
        existing_post = db_cursor.fetchone()
        
        if not existing_post:
            raise HTTPException(status_code=404, detail="Gönderi bulunamadı")
        else:
            post_dict = post.dict()
            for key, value in post_dict.items():
                if value:
                    sql = f"UPDATE posts SET {key} = %s WHERE post_id = %s"
                    values = (value, post_id)
                    db_cursor.execute(sql, values)
                    db_connection.commit()
            return {"message": f"Gönderi başarıyla güncellendi! Güncellenmiş veri: {str(post)}"}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()

# Gönderi silme işlemi
@router.delete("/delete/{post_id}")
async def delete_post(post_id: int):
    db_connection = get_database_connection()
    db_cursor = db_connection.cursor()
    try:
        # Gönderi kontrolü
        db_cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
        existing_post = db_cursor.fetchone()
        if not existing_post:
            raise HTTPException(status_code=404, detail="Gönderi bulunamadı")

        # Gönderiyi sil
        db_cursor.execute("DELETE FROM posts WHERE post_id = %s", (post_id,))
        db_connection.commit()
        
        # id sütununu yeniden sıralıyoruz
        db_cursor.execute("SET @count = 0;")
        db_cursor.execute("UPDATE posts SET id = @count:= @count + 1;")
        db_cursor.execute("ALTER TABLE posts AUTO_INCREMENT = 1;")
        db_connection.commit()
        
        return {"message": "Gönderi silindi! Silinen gönderi:" + str(existing_post)}
    except Error as db_error:
        raise HTTPException(status_code=500, detail=f"Veri tabanı hatası: {db_error}")
    finally:
        db_cursor.close()
        db_connection.close()