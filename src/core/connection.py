import mysql.connector
from src.core.database import DatabaseConfig


def get_connection():
    """
    Bu fonksiyon, MySQL veritabanına bağlantı oluşturmak için kullanılır.
    Başarılı olması durumunda bağlantı nesnesini döndürür,
    hata oluşursa None değeri döndürülür.
    """

    try:
        # Veritabanı bağlantısı oluşturuluyor
        connection = mysql.connector.connect(
            host=DatabaseConfig.host,          # Veritabanı sunucu adresi (örn: localhost)
            user=DatabaseConfig.user,          # Veritabanı kullanıcı adı
            password=DatabaseConfig.password,  # Kullanıcıya ait şifre
            database=DatabaseConfig.name,      # Bağlanılacak veritabanı adı
            auth_plugin='mysql_native_password'  # MySQL kimlik doğrulama yöntemi
        )

        # Bağlantı başarılı ise connection nesnesi döndürülür
        return connection

    except mysql.connector.Error as err:
        # Bağlantı sırasında hata oluşursa hata mesajı yazdırılır
        print("Veritabanı bağlantı hatası:", err)

        # Hata durumunda None döndürülür
        return None