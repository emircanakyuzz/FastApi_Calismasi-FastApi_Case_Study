# FastAPI ile RESTful Backend Geliştirme
### Kullanılan Teknolojiler
- FastAPI: Backend uygulamasının geliştirilmesi için.
- Uvicorn: FastAPI uygulamasını çalıştırmak için.
- MySQL: Veritabanı işlemleri için.
- CORS Middleware: Farklı kökenlerden gelen isteklere izin vermek için.
- HTTP Metodları: GET, POST, PUT, PATCH, DELETE kullanılarak RESTful işlemler gerçekleştirildi.

### Backend:
- FastAPI kullanılarak servis API'leri oluşturuldu.
- CRUD işlemleri (Create, Retrieve, Update, Delete) eksiksiz bir şekilde uygulandı.
- Uvicorn sunucusu ile FastAPI çalıştırılarak API, hızlı ve güvenilir bir şekilde sunuldu.
- Tüm API işlemleri için HTTP metodları (GET, POST, PUT, PATCH, DELETE) kullanıldı.
### CORS Desteği:
- API'ye farklı kökenlerden gelen isteklerin organize edilmesi için kullanılan CORS (Cross-Origin Resource Sharing) yapılandırıldı fakat detaylandırılmadı.
### RESTful API:
- API yapısı, RESTful prensiplere uygun olarak tasarlandı.
- Belirli endpoint'ler (örneğin, /users, /posts) üzerinden veri işleme işlemleri gerçekleştirildi.

### Endpointler (/users):
1. Kullanıcı İşlemleri (/users):
- POST /users/: Yeni kullanıcı oluşturma.
- GET /users/{user_id}: Kullanıcı bilgilerini görüntüleme.
- PATCH /users/{user_id}: Kullanıcı bilgilerini güncelleme.
- DELETE /users/{user_id}: Kullanıcıyı silme.
2. Gönderi İşlemleri (/posts):
- POST /posts/: Yeni gönderi oluşturma.
- GET /posts/: Tüm gönderileri görüntüleme.
- GET /posts/{post_id}: Belirli bir gönderiyi görüntüleme.
- PATCH /posts/{post_id}: Gönderiyi güncelleme.
- DELETE /posts/{post_id}: Gönderiyi silme.

### Proje Kurulumu ve Uygulamayı Başlatma:
- Gerekli Pakelerin Kurulumu: "pip install fastapi uvicorn mysql-connector-python"
- Uygulamayı Başlatma: "uvicorn main:app --reload"

