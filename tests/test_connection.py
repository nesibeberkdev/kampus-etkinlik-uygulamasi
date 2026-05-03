from src.core.connection import get_connection


def test_database_connection():
    """
    Veritabanı bağlantısının kurulup kurulamadığını kontrol eder.
    """

    connection = get_connection()

    assert connection is not None

    connection.close()