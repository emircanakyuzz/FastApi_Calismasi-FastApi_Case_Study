import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.user import router as user_router
from routes.post import router as post_router

app = FastAPI() # Tüm endpoint noktalarını bağlayacağımız genel API

# API'ye erişim izni verilen adreslerin tanımlanması
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins, # İzin verilen adresler
    allow_credentials = True, # Çerezlere izin ver
    allow_methods=["GET", "POST", "PUT", "DELETE"], # İzin verilen HTTP metodları
    allow_headers=["*"],  # İzin verilen başlıklar
)

app.include_router(auth_router, tags=["Authentication"])
app.include_router(user_router, tags=["Users"])
app.include_router(post_router, tags=["Posts"])

@app.get("/")
async def root():
    return {"Message": "API Çalışıyor!"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000)