from core.connection import get_connection


def get_all_events():
    """
    Veritabanındaki etkinlikleri listeler.
    """

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT id, title, description, date, location, capacity, image_filename
        FROM events
    """

    cursor.execute(query)
    events = cursor.fetchall()

    cursor.close()
    connection.close()

    return events



#admin panelinde etkinlikleri yönetebilmek yani düzenlemek için:

def get_event_by_id(event_id):
    """
    ID bilgisine göre etkinlik kaydını getirir.
    """

    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        query = """
            SELECT id, title, description, date, location, capacity, image_filename
            FROM events
            WHERE id = %s
        """

        cursor.execute(query, (event_id,))
        event = cursor.fetchone()

        return event

    except Exception:
        return None

    finally:
        cursor.close()
        connection.close()


def update_event(event_id, title, description, date, location, capacity, image_filename):
    """
    Etkinlik bilgilerini günceller.
    """

    connection = get_connection()

    if connection is None:
        return False, "Veritabanı bağlantısı kurulamadı."

    cursor = connection.cursor()

    try:
        query = """
            UPDATE events
            SET title = %s,
                description = %s,
                date = %s,
                location = %s,
                capacity = %s,
                image_filename = %s
            WHERE id = %s
        """

        values = (
            title,
            description,
            date,
            location,
            capacity,
            image_filename,
            event_id
        )

        cursor.execute(query, values)
        connection.commit()

        return True, "Etkinlik başarıyla güncellendi."

    except Exception:
        return False, "Etkinlik güncellenirken bir hata oluştu."

    finally:
        cursor.close()
        connection.close()

#etkinlik ekle-sil
def add_event(title, description, date, location, capacity, image_filename):
    """
    Yeni etkinlik kaydı oluşturur.
    """

    connection = get_connection()

    if connection is None:
        return False, "Veritabanı bağlantısı kurulamadı."

    cursor = connection.cursor()

    try:
        query = """
            INSERT INTO events (title, description, date, location, capacity, image_filename)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            title,
            description,
            date,
            location,
            capacity,
            image_filename
        )

        cursor.execute(query, values)
        connection.commit()

        return True, "Etkinlik başarıyla eklendi."

    except Exception:
        return False, "Etkinlik eklenirken bir hata oluştu."

    finally:
        cursor.close()
        connection.close()


def delete_event(event_id):
    """
    Seçilen etkinlik kaydını siler.
    """

    connection = get_connection()

    if connection is None:
        return False, "Veritabanı bağlantısı kurulamadı."

    cursor = connection.cursor()

    try:
        query = """
            DELETE FROM events
            WHERE id = %s
        """

        cursor.execute(query, (event_id,))
        connection.commit()

        return True, "Etkinlik başarıyla silindi."

    except Exception:
        return False, "Etkinlik silinirken bir hata oluştu."

    finally:
        cursor.close()
        connection.close()