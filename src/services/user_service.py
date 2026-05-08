import bcrypt

from core.connection import get_connection #MySQL veri tabanına baglantı açmak.


def is_email_registered(email):
    """
    Girilen e-posta adresinin sistemde kayıtlı olup olmadığını kontrol eder.
    Kayıt varsa True, yoksa False döndürür.
    """

    connection = get_connection() #get_connection : bağlantı oluşturuluyor.
    #connection = get_connection() : connection.py dosyasındaki bağlantı ayarlarını kullan ve MySQL'e bağlan.

    if connection is None:
        return False

    cursor = connection.cursor()

    query = """
        SELECT id
        FROM users
        WHERE email = %s
    """

    cursor.execute(query, (email,))
    result = cursor.fetchone()#bulduğun ilk sonucu getir.

    cursor.close()
    connection.close()

    return result is not None


def register_user(username, email, password, role="user"):
    """
    Yeni kullanıcı kaydı oluşturur.
    Kullanıcı şifresi veritabanına kaydedilmeden önce hashlenir.
    """

    if is_email_registered(email):
        return False, "Bu e-posta adresi ile daha önce kayıt oluşturuldu."

    connection = get_connection()

    if connection is None:
        return False, "Veritabanı bağlantısı kurulamadı."

    cursor = connection.cursor()

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    query = """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
    """

    values = (username, email, password_hash, role)

    try:
        cursor.execute(query, values)
        connection.commit()
        return True, "Kullanıcı kaydı başarıyla oluşturuldu."

    except Exception:
        return False, "Kayıt işlemi sırasında bir hata oluştu."

    finally:
        cursor.close()
        connection.close()


def login_user(email, password):
    """
    Kullanıcının giriş bilgilerini kontrol eder.
    E-posta ve şifre doğruysa True döndürür.
    """

    connection = get_connection()

    if connection is None:
        return False, "Veritabanı bağlantısı kurulamadı."

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, username, email, password_hash, role
        FROM users
        WHERE email = %s
    """

    try:
        cursor.execute(query, (email,))
        user = cursor.fetchone()

        if user is None:
            return False, "Bu e-posta adresine ait kullanıcı bulunamadı."

        saved_password_hash = user["password_hash"]

        if isinstance(saved_password_hash, str):
            saved_password_hash = saved_password_hash.encode("utf-8")

        is_password_correct = bcrypt.checkpw(
            password.encode("utf-8"),
            saved_password_hash
        )

        if not is_password_correct:
            return False, "Şifre hatalıdır."

        return True, "Giriş işlemi başarılı."

    except Exception:
        return False, "Giriş işlemi sırasında bir hata oluştu."

    finally:
        cursor.close()
        connection.close()


def get_user_by_email(email):
    """
    E-posta adresine göre kullanıcı bilgisini getirir.
    Session kontrolü ve etkinliğe katılım işlemlerinde kullanılır.
    """

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, username, email, role
        FROM users
        WHERE email = %s
    """

    try:
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        return user

    except Exception:
        return None

    finally:
        cursor.close()
        connection.close()