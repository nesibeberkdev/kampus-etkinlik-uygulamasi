from src.core.connection import get_connection


def get_all_events():
    """
    Veritabanındaki tüm etkinlikleri getirir.
    """

    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM events"
    cursor.execute(query)
    events = cursor.fetchall()

    cursor.close()
    connection.close()

    return events