from src.services.participation_service import is_already_participated


def test_participation_check():
    """
    Katılım kontrol fonksiyonunun hata vermeden çalıştığını test eder.
    """

    result = is_already_participated(1, 1)

    assert result in [True, False]