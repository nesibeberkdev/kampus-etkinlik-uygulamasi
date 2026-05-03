from src.services.user_service import register_user


def test_register_user_with_empty_data():
    """
    Boş veri ile kullanıcı kaydı yapılmaya çalışıldığında
    sistemin hata vermesi beklenir.
    """

    success, message = register_user("", "", "")

    assert success is False