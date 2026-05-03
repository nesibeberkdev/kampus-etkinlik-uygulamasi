from src.core.connection import get_connection


def add_participation(user_id, event_id):
    """
    Kullanıcının etkinliğe katılmasını sağlar.
    Aynı etkinliğe tekrar katılımı engeller.
    """

    connection = get_connection()

    if connection is None:
        return False, "Veritabanı bağlantısı kurulamadı."

    cursor = connection.cursor(dictionary=True)

    try:
        check_query = """
            SELECT id
            FROM participation
            WHERE user_id = %s AND event_id = %s
        """
        cursor.execute(check_query, (user_id, event_id))
        existing_participation = cursor.fetchone()

        if existing_participation is not None:
            return False, "Bu etkinliğe zaten katıldınız."

        insert_query = """
            INSERT INTO participation (user_id, event_id)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (user_id, event_id))
        connection.commit()

        return True, "Etkinliğe başarıyla katıldınız."

    except Exception:
        return False, "Katılım işlemi sırasında bir hata oluştu."

    finally:
        cursor.close()
        connection.close()


def leave_participation(user_id, event_id):
    """
    Kullanıcının etkinlik katılımını iptal eder.
    """

    connection = get_connection()

    if connection is None:
        return False, "Veritabanı bağlantısı kurulamadı."

    cursor = connection.cursor()

    try:
        delete_query = """
            DELETE FROM participation
            WHERE user_id = %s AND event_id = %s
        """
        cursor.execute(delete_query, (user_id, event_id))
        connection.commit()

        return True, "Etkinlik katılımı iptal edildi."

    except Exception:
        return False, "Etkinlik iptali sırasında bir hata oluştu."

    finally:
        cursor.close()
        connection.close()


def get_user_joined_events(user_id):
    """
    Kullanıcının katıldığı etkinlikleri listeler.
    """

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT e.id, e.title, e.description, e.date, e.location, e.capacity, e.image_filename
        FROM participation p
        INNER JOIN events e ON p.event_id = e.id
        WHERE p.user_id = %s
    """

    cursor.execute(query, (user_id,))
    events = cursor.fetchall()

    cursor.close()
    connection.close()

    return events