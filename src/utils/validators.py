def is_empty_field(value):
    """
    Girilen değerin boş olup olmadığını kontrol eder.
    """
    return value is None or str(value).strip() == ""


def is_valid_email(email):
    """
    E-posta adresinin temel olarak geçerli formatta olup olmadığını kontrol eder.
    """
    return "@" in email and "." in email