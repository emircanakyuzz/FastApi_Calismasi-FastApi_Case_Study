from pydantic import BaseModel
from typing import Optional
import datetime as dt

# USER CRUD
class CreateUser (BaseModel): # Kayıt olan kullanıcı için şema
    name: str
    surname: str
    mail: str
    password: str
    date: dt.date
    sex: str
    
class LoginUser(BaseModel): # Giriş yapan kullanıcı için şema
    mail: str
    password: str

class UpdateUser(BaseModel): # Kullanıcı profili güncelleme için şema
    name: Optional[str]
    surname: Optional[str]
    mail: Optional[str]
    password: Optional[str]
    date: Optional[dt.date]
    sex: Optional[str]
    
class DeleteUser(BaseModel): # Kullanıcı profili silme için şema
    user_id: int
    
class RetrieveUser(BaseModel): # Kullanıcı profili görüntüleme için şema
    user_id: int

# POST CRUD
class CreatePost(BaseModel): # Post oluşturma için şema
    title: str
    contents: str
    date: dt.date
    
class UpdatePost(BaseModel): # Post güncelleme için şema
    title: Optional[str]
    contents: Optional[str]
    
class DeletePost(BaseModel): # Post silme için şema
    post_id: int

class RetrievePost(BaseModel): # Post görüntüleme için şema
    post_id: int